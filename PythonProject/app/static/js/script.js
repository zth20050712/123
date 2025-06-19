document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('image');
    const previewImage = document.getElementById('preview-image');
    const submitButton = document.querySelector('button[type="submit"]');

    if (fileInput && previewImage) {
        fileInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    previewImage.src = e.target.result;
                    previewImage.style.display = 'block';
                    if (submitButton) submitButton.disabled = false;
                };
                reader.readAsDataURL(this.files[0]);
            } else {
                previewImage.src = '';
                previewImage.style.display = 'none';
                if (submitButton) submitButton.disabled = true;
            }
        });
    }
});