// epitag/public/js/qr_scanner.js

frappe.provide('epitag.scanning');

epitag.scanning.QRScanner = class QRScanner {
    constructor(opts) {
        this.callback = opts.callback || function() {};
        this.target_field = opts.target_field;
        this.dialog = null;
        this.stream = null;
    }

    async init() {
        // Load jsQR library if not already loaded
        if (!window.jsQR) {
            await frappe.require([
                'https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.min.js'
            ]);
        }
    }

    async show() {
        await this.init();

        this.dialog = new frappe.ui.Dialog({
            title: __('Scan QR Code'),
            fields: [
                {
                    fieldname: 'video_preview',
                    fieldtype: 'HTML',
                    options: `
                        <div class="qr-scanner-container">
                            <video id="qr-video" playsinline style="width: 100%; max-width: 400px;"></video>
                            <div class="scan-region-highlight"></div>
                            <div class="scan-region-highlight-svg"></div>
                        </div>
                        <div class="qr-status mt-3"></div>
                    `
                }
            ],
            primary_action_label: __('Close'),
            primary_action: () => {
                this.stop();
                this.dialog.hide();
            }
        });

        this.dialog.show();
        await this.start();
    }

    async start() {
        try {
            // Request camera access
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: "environment" }
            });

            const video = document.getElementById('qr-video');
            video.srcObject = this.stream;
            video.play();

            // Start scanning
            requestAnimationFrame(() => this.scan());

        } catch (err) {
            frappe.msgprint({
                title: __('Camera Access Error'),
                message: __('Please ensure camera permissions are granted and try again.'),
                indicator: 'red'
            });
            console.error('Camera access error:', err);
        }
    }

    stop() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }
    }

    scan() {
        if (!this.stream) return;

        const video = document.getElementById('qr-video');
        if (video.readyState === video.HAVE_ENOUGH_DATA) {
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            
            const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
            const code = jsQR(imageData.data, imageData.width, imageData.height);

            if (code) {
                // QR Code found
                this.stop();
                this.dialog.hide();
                this.callback(code.data);

                // If target field is specified, update it
                if (this.target_field) {
                    frappe.model.set_value(
                        this.target_field.doctype,
                        this.target_field.docname,
                        this.target_field.fieldname,
                        code.data
                    );
                }

                frappe.show_alert({
                    message: __('QR Code scanned successfully'),
                    indicator: 'green'
                });
            }
        }

        // Continue scanning
        if (this.stream) {
            requestAnimationFrame(() => this.scan());
        }
    }
}

// Add scan button to relevant fields
frappe.form.link_formatters['Item'] = function(value, doc) {
    if (!value) return '';
    
    let html = value;
    if (frappe.form.link_formatters['Item'].scan_button !== false) {
        html += ` <button class="btn btn-xs btn-default scan-qr-code">
            ${frappe.utils.icon('scan', 'xs')}
            ${__('Scan')}
        </button>`;
    }
    return html;
};

// Initialize scanner when scan button is clicked
$(document).on('click', '.scan-qr-code', function() {
    const field = $(this).closest('[data-fieldname]');
    const doctype = field.attr('data-doctype');
    const docname = field.closest('[data-name]').attr('data-name');
    const fieldname = field.attr('data-fieldname');

    const scanner = new epitag.scanning.QRScanner({
        target_field: {
            doctype: doctype,
            docname: docname,
            fieldname: fieldname
        }
    });
    scanner.show();
});