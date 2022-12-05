function onDragStart(event) {
    event
        .dataTransfer
        .setData('text/plain', event.target.id); // Change "text/plain" to simply "text" for internet explorer 9 - 11

    event
        .currentTarget
        .style
        .backgroundColor = 'yellow';
}

function onDragOver(event) {
    event.preventDefault();
}

function onDrop(event) {
    const id = event
    .dataTransfer
    .getData('text');

    const draggableElement = document.getElementById(id);
    const dropzone = event.target;
    dropzone.appendChild(draggableElement);

    event
        .dataTransfer
        .clearData();
}



// function onDragEnd(event) {}