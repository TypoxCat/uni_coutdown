const canvas = document.getElementById("snake");
const ctx = canvas.getContext("2d");

const fishImg = new Image();
fishImg.src = "cloth_winter.png";

fishImg.onload = () => {
    ctx.drawImage(fishImg, 100, 100, 40, 40);
    console.log("✅ Image drawn");
};

fishImg.onerror = () => {
    console.error("❌ Failed to load image");
};
