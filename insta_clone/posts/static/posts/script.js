// ---------------- SIGNUP ----------------

async function signupUser() {
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const res = await fetch('/api/register/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username, email, password})
    });

    if(res.ok){
        alert('User Created!');
        document.getElementById('signupForm').reset();
    } else {
        alert('Signup failed!');
    }
}

document.getElementById('signupForm').onsubmit = (e) => {
    e.preventDefault();
    signupUser();
};


// ---------------- CREATE POST ----------------

document.getElementById('postForm').onsubmit = async (e) => {
    e.preventDefault();

    const image = document.getElementById('postImage').files[0];
    const caption = document.getElementById('caption').value;

    const formData = new FormData();
    if(image) formData.append('image', image);
    formData.append('caption', caption);

    const res = await fetch('/api/posts/', {
        method: 'POST',
        body: formData
    });

    if(res.ok){
        alert('Post created!');
        document.getElementById('postForm').reset();
        loadFeed();
    } else {
        alert('Error creating post');
    }
};


// ---------------- LOAD POSTS FEED ----------------

async function loadFeed(){
    const res = await fetch('/api/posts/');
    const data = await res.json();

    const feedDiv = document.getElementById('feed');
    feedDiv.innerHTML = '';

    data.forEach(post => {

        const postDiv = document.createElement('div');
        postDiv.classList.add('post');

        let imgHTML = post.image ? `<img src="${post.image}" width="300"/>` : '';

        postDiv.innerHTML = `
            <strong>${post.user.username}</strong><br>
            ${imgHTML}<br>
            ${post.caption}
            <hr>
        `;

        feedDiv.appendChild(postDiv);
    });
}


// ---------------- STORIES ----------------

async function loadStories(){

    const res = await axios.get('/api/stories/');
    const stories = res.data;

    const container = document.getElementById('stories');
    container.innerHTML='';

    stories.forEach(story=>{
        container.innerHTML+=`
        <img src="/media/${story.image}" width="80"
        style="border-radius:50%;margin:10px;">
        `;
    });
}

async function uploadStory(){

    const file=document.getElementById('storyImage').files[0];

    let formData=new FormData();

    formData.append("image",file);

    await axios.post('/api/stories/',formData);

    loadStories();
}


// ---------------- CHAT (WEBSOCKET) ----------------

const socket = new WebSocket(
    "ws://" + window.location.host + "/ws/chat/"
);

socket.onmessage = function(e){

    const data = JSON.parse(e.data);

    const chatBox = document.getElementById("chatBox");

    chatBox.innerHTML += "<p>"+data.message+"</p>";
};

function sendMessage(){

    const input = document.getElementById("chatMessage");

    socket.send(JSON.stringify({
        "message": input.value
    }));

    input.value="";
}


// ---------------- INITIAL LOAD ----------------

loadStories();
loadFeed();