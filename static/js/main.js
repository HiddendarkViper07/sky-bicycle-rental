// static/js/main.js

/**
 * Show message in live message div
 */
function showMessage(message, type = 'info') {
    const msgDiv = document.getElementById('liveMessage');
    if (!msgDiv) return;
    
    const icon = type === 'error' ? 'exclamation-circle' : 
                 type === 'success' ? 'check-circle' : 'circle-info';
    
    msgDiv.innerHTML = `<i class="fas fa-${icon}"></i> ${message}`;
    
    // Set background color based on type
    if (type === 'error') {
        msgDiv.style.background = '#f8d7da';
        msgDiv.style.borderLeftColor = '#dc3545';
    } else if (type === 'success') {
        msgDiv.style.background = '#d4edda';
        msgDiv.style.borderLeftColor = '#28a745';
    } else {
        msgDiv.style.background = '#e7f1fe';
        msgDiv.style.borderLeftColor = '#0f2b43';
    }
}

/**
 * Format Aadhar number (XXXX XXXX XXXX)
 */
function formatAadhar(input) {
    let value = input.value.replace(/\s/g, '').replace(/\D/g, '');
    if (value.length > 12) value = value.slice(0, 12);
    
    let parts = [];
    for (let i = 0; i < value.length; i += 4) {
        parts.push(value.slice(i, i + 4));
    }
    
    input.value = parts.join(' ');
}

/**
 * Validate mobile number (10 digits)
 */
function validateMobile(mobile) {
    return /^\d{10}$/.test(mobile);
}

/**
 * Validate Aadhar number (12 digits with optional spaces)
 */
function validateAadhar(aadhar) {
    const cleaned = aadhar.replace(/\s/g, '');
    return /^\d{12}$/.test(cleaned);
}

/**
 * Validate age (18-100)
 */
function validateAge(age) {
    age = parseInt(age);
    return !isNaN(age) && age >= 18 && age <= 100;
}

/**
 * Validate hours (1-24)
 */
function validateHours(hours) {
    hours = parseInt(hours);
    return !isNaN(hours) && hours >= 1 && hours <= 24;
}

/**
 * Get current location using geolocation
 */
function getCurrentLocation() {
    return new Promise((resolve, reject) => {
        if (!navigator.geolocation) {
            reject(new Error('Geolocation not supported'));
            return;
        }
        
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const lat = position.coords.latitude.toFixed(6);
                const lng = position.coords.longitude.toFixed(6);
                resolve(`📍 ${lat}, ${lng}`);
            },
            (error) => {
                let message = 'Location access denied';
                if (error.code === 1) {
                    message = 'Location permission denied';
                } else if (error.code === 2) {
                    message = 'Location unavailable';
                } else if (error.code === 3) {
                    message = 'Location request timeout';
                }
                reject(new Error(message));
            }
        );
    });
}

/**
 * Download receipt as text file
 */
function downloadReceipt(bookingData) {
    const receipt = generateReceiptText(bookingData);
    const blob = new Blob([receipt], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `SkyBicycle_${bookingData.ticket_id}.txt`;
    a.click();
    window.URL.revokeObjectURL(url);
}

/**
 * Generate receipt text content
 */
function generateReceiptText(booking) {
    const line = '='.repeat(40);
    const separator = '-'.repeat(40);
    
    return `
${line}
        SKY BICYCLE RENTAL
          BOOKING TICKET
${line}

Ticket No: ${booking.ticket_id}
Date: ${new Date().toLocaleDateString()}
${separator}

CUSTOMER DETAILS
${separator}
Name: ${booking.full_name}
Mobile: ${booking.mobile}
Aadhar: XXX-XXXX-${booking.aadhar_number.slice(-4)}

RENTAL DETAILS
${separator}
Date: ${booking.rent_date}
Time: ${booking.rent_time}
Duration: ${booking.hours} hours
Location: ${booking.location}

PAYMENT DETAILS
${separator}
Total Amount: ₹${booking.total_amount}
Paid Now: ₹${booking.paid_amount}
Balance Due: ₹${booking.balance_amount}
Payment ID: ${booking.payment_id || 'N/A'}

STATUS: ${booking.status.toUpperCase()}
${separator}

Please show this ticket at pickup.
Valid only on booking date.

Thank you for choosing Sky Bicycle!
${line}
    `;
}

/**
 * Print receipt
 */
function printReceipt(booking) {
    const printWindow = window.open('', '_blank');
    
    printWindow.document.write(`
        <html>
            <head>
                <title>Sky Bicycle Ticket - ${booking.ticket_id}</title>
                <style>
                    body { font-family: 'Courier New', monospace; padding: 20px; max-width: 400px; margin: 0 auto; }
                    .ticket { border: 2px dashed #000; padding: 20px; }
                    h2 { text-align: center; margin-top: 0; }
                    .header { text-align: center; margin-bottom: 20px; }
                    .details { margin: 20px 0; }
                    .row { display: flex; justify-content: space-between; margin: 5px 0; }
                    .footer { text-align: center; margin-top: 20px; font-size: 12px; }
                    hr { border: 1px dashed #000; }
                </style>
            </head>
            <body>
                <div class="ticket">
                    <div class="header">
                        <h2>SKY BICYCLE RENTAL</h2>
                        <p>Booking Ticket</p>
                    </div>
                    
                    <hr>
                    
                    <div class="details">
                        <div class="row"><span>Ticket No:</span> <strong>${booking.ticket_id}</strong></div>
                        <div class="row"><span>Name:</span> ${booking.full_name}</div>
                        <div class="row"><span>Mobile:</span> ${booking.mobile}</div>
                        <div class="row"><span>Date:</span> ${booking.rent_date}</div>
                        <div class="row"><span>Time:</span> ${booking.rent_time}</div>
                        <div class="row"><span>Hours:</span> ${booking.hours}</div>
                        <div class="row"><span>Location:</span> ${booking.location.substring(0, 20)}</div>
                    </div>
                    
                    <hr>
                    
                    <div class="details">
                        <div class="row"><span>Total Amount:</span> ₹${booking.total_amount}</div>
                        <div class="row"><span>Paid Now:</span> ₹${booking.paid_amount}</div>
                        <div class="row"><span>Balance:</span> ₹${booking.balance_amount}</div>
                    </div>
                    
                    <hr>
                    
                    <div class="footer">
                        <p>Show this ticket at pickup</p>
                        <p style="font-size: 10px;">Valid on booking date only</p>
                    </div>
                </div>
            </body>
        </html>
    `);
    
    printWindow.document.close();
    printWindow.focus();
    printWindow.print();
}

/**
 * Initialize date inputs with today's date
 */
function initializeDateInputs() {
    const dateInputs = document.querySelectorAll('input[type="date"]');
    const today = new Date().toISOString().split('T')[0];
    
    dateInputs.forEach(input => {
        if (!input.value) {
            input.value = today;
        }
    });
}

/**
 * Initialize time inputs with current time
 */
function initializeTimeInputs() {
    const timeInputs = document.querySelectorAll('input[type="time"]');
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const currentTime = `${hours}:${minutes}`;
    
    timeInputs.forEach(input => {
        if (!input.value) {
            input.value = currentTime;
        }
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeDateInputs();
    initializeTimeInputs();
    
    // Add Aadhar formatting
    const aadharInputs = document.querySelectorAll('input[name="aadhar_number"], #id_aadhar_number');
    aadharInputs.forEach(input => {
        input.addEventListener('input', function() {
            formatAadhar(this);
        });
    });
    
    // Mobile number validation
    const mobileInputs = document.querySelectorAll('input[name="mobile"], #id_mobile');
    mobileInputs.forEach(input => {
        input.addEventListener('input', function() {
            this.value = this.value.replace(/\D/g, '').slice(0, 10);
        });
    });
    
    // Get location button
    const locationBtn = document.getElementById('getLocationBtn');
    if (locationBtn) {
        locationBtn.addEventListener('click', async function() {
            try {
                const location = await getCurrentLocation();
                const locationInput = document.getElementById('id_location') || 
                                     document.querySelector('textarea[name="location"]');
                if (locationInput) {
                    locationInput.value = location;
                    showMessage('Location captured!', 'success');
                }
            } catch (error) {
                showMessage(error.message, 'error');
            }
        });
    }
});