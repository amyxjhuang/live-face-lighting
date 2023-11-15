import * as THREE from 'three';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

const renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight, false );
document.body.appendChild( renderer.domElement );

const geometry = new THREE.BoxGeometry( 1, 1, 1 );
const material = new THREE.MeshBasicMaterial( { color: 0x00ff00 } );
const cube = new THREE.Mesh( geometry, material );
scene.add( cube );


// const geometry = new THREE.SphereGeometry(1, 32, 32);
// const material = new THREE.MeshBasicMaterial({ color: 0xff0000 });
// const ball = new THREE.Mesh(geometry, material);

// scene.add( ball );

camera.position.z = 5;

let isProcessing = false;


function startProcessingFace() {
    isProcessing = true;
    fetch('http://127.0.0.1:5001/start_processing')
}
function stopProcessingFace() {
    isProcessing = false;
    fetch('http://127.0.0.1:5001/stop_processing')
}

// Function to make a GET request to the Flask API endpoint
function getFaceData() {
    if (!isProcessing) {
        return;
    }
    return fetch('http://127.0.0.1:5001/get_face_data')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Process the received face data
            console.log(data);

            // Update Three.js scene based on the received data
            cube.rotation.x = data.x;
            cube.rotation.y = data.y;
            // Add more updates as needed based on your API response

        })
        .catch(error => {
            console.error('Error fetching face data:', error);
        });
}

function animateScene() {
    console.log("animate", isProcessing)
    requestAnimationFrame(animateScene);
    if (isProcessing) {
        getFaceData();
    }
    // cube.rotation.x += 0.01 
    // cube.rotation.y += 0.01
    renderer.render(scene, camera);
}

animateScene(); // creates a loop to draw scene 