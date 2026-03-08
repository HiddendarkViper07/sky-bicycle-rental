// static/js/payment.js

/**
 * Initialize Razorpay payment
 */
function initializeRazorpay(options) {
    return new Promise((resolve, reject) => {
        try {
            const razorpay = new Razorpay(options);
            
            razorpay.on('payment.success', function(response) {
                resolve(response);
            });
            
            razorpay.on('payment.error', function(error) {
                reject(error);
            });
            
            razorpay.on('modal.close', function() {
                reject(new Error('Payment modal closed'));
            });
            
            razorpay.open();
        } catch (error) {
            reject(error);
        }
    });
}

/**
 * Process payment with Razorpay
 */
async function processPayment(paymentData) {
    const {
        key,
        amount,
        orderId,
        name,
        description,
        prefill,
        notes
    } = paymentData;
    
    const options = {
        key: key,
        amount: amount * 100, // Convert to paise
        currency: "INR",
        name: name || "Sky Bicycle Rental",
        description: description || "Booking Advance Payment",
        order_id: orderId,
        image: "https://cdn.razorpay.com/icons/icon-ios.png",
        handler: function(response) {
            return response;
        },
        prefill: prefill || {
            name: "",
            contact: ""
        },
        notes: notes || {},
        theme: {
            color: "#0f2b43"
        },
        modal: {
            ondismiss: function() {
                console.log('Payment modal dismissed');
            }
        }
    };
    
    return new Promise((resolve, reject) => {
        try {
            const razorpayInstance = new Razorpay(options);
            
            razorpayInstance.on('payment.success', function(response) {
                resolve(response);
            });
            
            razorpayInstance.on('payment.error', function(response) {
                reject(response.error);
            });
            
            razorpayInstance.open();
        } catch (error) {
            reject(error);
        }
    });
}

/**
 * Verify payment signature
 */
function verifyPaymentSignature(response) {
    const {
        razorpay_payment_id,
        razorpay_order_id,
        razorpay_signature
    } = response;
    
    // Send to server for verification
    return fetch('/payment-callback/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            razorpay_payment_id,
            razorpay_order_id,
            razorpay_signature
        })
    })
    .then(response => response.json())
    .catch(error => {
        console.error('Verification error:', error);
        throw error;
    });
}

/**
 * Get CSRF token from cookies
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Format currency in Indian format
 */
function formatIndianCurrency(amount) {
    const formatter = new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    });
    
    return formatter.format(amount);
}

/**
 * Validate payment amount
 */
function validatePaymentAmount(amount) {
    amount = parseInt(amount);
    if (isNaN(amount) || amount <= 0) {
        return { valid: false, message: 'Invalid amount' };
    }
    return { valid: true, amount: amount };
}

/**
 * Generate receipt HTML
 */
function generateReceiptHTML(booking) {
    return `
        <div class="receipt-card">
            <div class="receipt-header">
                <div class="success-icon">
                    <i class="fas fa-check-circle"></i>
                </div>
                <h2>Sky Bicycle Rental</h2>
                <p>Booking Confirmed • E-Ticket</p>
            </div>
            
            <div class="receipt-highlight">
                <div class="label">Ticket Number</div>
                <div class="ticket-id">${booking.ticket_id}</div>
            </div>
            
            <div class="receipt-body">
                <div class="receipt-field">
                    <div class="label">Name</div>
                    <div class="value">${booking.full_name}</div>
                </div>
                <div class="receipt-field">
                    <div class="label">Mobile</div>
                    <div class="value">${booking.mobile}</div>
                </div>
                <div class="receipt-field">
                    <div class="label">Date</div>
                    <div class="value">${booking.rent_date}</div>
                </div>
                <div class="receipt-field">
                    <div class="label">Time</div>
                    <div class="value">${booking.rent_time}</div>
                </div>
                <div class="receipt-field">
                    <div class="label">Hours</div>
                    <div class="value">${booking.hours}</div>
                </div>
                <div class="receipt-field">
                    <div class="label">Paid</div>
                    <div class="value">₹${booking.paid_amount}</div>
                </div>
            </div>
        </div>
    `;
}