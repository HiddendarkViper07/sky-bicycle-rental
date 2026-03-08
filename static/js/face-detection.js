// static/js/face-detection.js

let cameraStream = null;
let faceDetectionModel = null;
let faceDetected = false;
let detectionInterval = null;

/**
 * Load the face detection model
 */
async function loadFaceDetectionModel() {
    try {
        faceDetectionModel = await blazeface.load();
        console.log('✅ Face detection model loaded successfully');
        return true;
    } catch (error) {
        console.error('❌ Error loading face model:', error);
        return false;
    }
}

/**
 * Start camera and begin face detection
 */
async function startCamera(videoElementId = 'cameraFeed') {
    const video = document.getElementById(videoElementId);
    
    try {
        cameraStream = await navigator.mediaDevices.getUserMedia({
            video: {
                facingMode: 'user',
                width: { ideal: 640 },
                height: { ideal: 480 },
                frameRate: { ideal: 30 }
            },
            audio: false
        });
        
        video.srcObject = cameraStream;
        video.style.display = 'block';
        
        // Wait for video to be ready
        await new Promise((resolve) => {
            video.onloadedmetadata = () => {
                video.play();
                resolve();
            };
        });
        
        // Start face detection
        startFaceDetection(videoElementId);
        
        return true;
    } catch (error) {
        console.error('❌ Camera error:', error);
        throw error;
    }
}

/**
 * Start face detection loop
 */
function startFaceDetection(videoElementId = 'cameraFeed', statusElementId = 'verificationStatus') {
    if (!faceDetectionModel) {
        console.warn('Face detection model not loaded');
        return;
    }
    
    const video = document.getElementById(videoElementId);
    const statusDiv = document.getElementById(statusElementId);
    
    // Clear any existing interval
    if (detectionInterval) {
        clearInterval(detectionInterval);
    }
    
    detectionInterval = setInterval(async () => {
        if (video.readyState === video.HAVE_ENOUGH_DATA && !video.paused) {
            try {
                const faces = await faceDetectionModel.estimateFaces(video, false);
                
                if (faces.length > 0) {
                    if (!faceDetected) {
                        faceDetected = true;
                        updateFaceDetectionStatus(true, statusDiv);
                        enableCaptureButton(true);
                    }
                } else {
                    if (faceDetected) {
                        faceDetected = false;
                        updateFaceDetectionStatus(false, statusDiv);
                        enableCaptureButton(false);
                    }
                }
            } catch (error) {
                console.error('Face detection error:', error);
            }
        }
    }, 500); // Check every 500ms
}

/**
 * Update face detection status display
 */
function updateFaceDetectionStatus(detected, statusDiv) {
    if (!statusDiv) return;
    
    if (detected) {
        statusDiv.innerHTML = '<i class="fas fa-check-circle" style="color: #1f8b4c;"></i> Face detected! You can capture now';
        statusDiv.style.background = '#d4edda';
        statusDiv.style.color = '#155724';
    } else {
        statusDiv.innerHTML = '<i class="fas fa-exclamation-circle" style="color: #b33f2f;"></i> No face detected. Please look at the camera';
        statusDiv.style.background = '#f8d7da';
        statusDiv.style.color = '#721c24';
    }
}

/**
 * Enable/disable capture button
 */
function enableCaptureButton(enable) {
    const captureBtn = document.getElementById('captureBtn');
    if (captureBtn) {
        captureBtn.disabled = !enable;
    }
}

/**
 * Capture selfie from video feed
 */
function captureSelfie(videoElementId = 'cameraFeed', canvasElementId = 'selfieCanvas', previewElementId = 'capturedPreview') {
    if (!faceDetected) {
        showMessage('Please ensure your face is visible', 'error');
        return false;
    }
    
    const video = document.getElementById(videoElementId);
    const canvas = document.getElementById(canvasElementId);
    const preview = document.getElementById(previewElementId);
    
    // Set canvas dimensions to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Draw video frame to canvas
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Convert to base64 image
    const imageData = canvas.toDataURL('image/jpeg', 0.9);
    
    // Update hidden input
    const selfieInput = document.getElementById('selfieImage');
    if (selfieInput) {
        selfieInput.value = imageData;
    }
    
    // Show preview
    if (preview) {
        preview.src = imageData;
        preview.style.display = 'block';
    }
    
    // Hide video
    video.style.display = 'none';
    
    // Show retake button
    const retakeBtn = document.getElementById('retakeBtn');
    if (retakeBtn) {
        retakeBtn.style.display = 'block';
    }
    
    // Disable capture button
    const captureBtn = document.getElementById('captureBtn');
    if (captureBtn) {
        captureBtn.disabled = true;
    }
    
    // Enable verify button
    const verifyBtn = document.getElementById('verifyBtn');
    if (verifyBtn) {
        verifyBtn.disabled = false;
    }
    
    // Stop camera stream
    stopCamera();
    
    return imageData;
}

/**
 * Retake selfie (clear and restart camera)
 */
function retakeSelfie(videoElementId = 'cameraFeed', previewElementId = 'capturedPreview') {
    const video = document.getElementById(videoElementId);
    const preview = document.getElementById(previewElementId);
    
    // Hide preview
    if (preview) {
        preview.style.display = 'none';
    }
    
    // Hide retake button
    const retakeBtn = document.getElementById('retakeBtn');
    if (retakeBtn) {
        retakeBtn.style.display = 'none';
    }
    
    // Clear selfie input
    const selfieInput = document.getElementById('selfieImage');
    if (selfieInput) {
        selfieInput.value = '';
    }
    
    // Disable verify button
    const verifyBtn = document.getElementById('verifyBtn');
    if (verifyBtn) {
        verifyBtn.disabled = true;
    }
    
    // Restart camera
    startCamera(videoElementId);
}

/**
 * Stop camera stream
 */
function stopCamera() {
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => {
            track.stop();
        });
        cameraStream = null;
    }
    
    if (detectionInterval) {
        clearInterval(detectionInterval);
        detectionInterval = null;
    }
}

/**
 * Check if camera is supported
 */
function isCameraSupported() {
    return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Load face detection model
    loadFaceDetectionModel();
    
    // Check camera support
    if (!isCameraSupported()) {
        const statusDiv = document.getElementById('verificationStatus');
        if (statusDiv) {
            statusDiv.innerHTML = '<i class="fas fa-exclamation-triangle" style="color: #b33f2f;"></i> Camera not supported on this device/browser';
        }
    }
});