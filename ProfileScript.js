// script.js
function previewImage(event) {
    const preview = document.getElementById('profile-preview');
    preview.style.display = 'block';
    preview.src = URL.createObjectURL(event.target.files[0]);
}
