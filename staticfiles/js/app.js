let groupActive = false; // is used to dtermine wheather to sumit as chat or to a group
let currentRecipient = '';
let chatInput = $('#chat-input');
let chatButton = $('#btn-send');
let userList = $('#user-list');
let messageList = $('#messages');

// groups
let groupList = $('#group-list');
let currentGroup = '';

function updateUserList() {
    $.getJSON('api/v1/user/', function (data) {
        userList.children('.user').remove();
        for (let i = 0; i < data.length; i++) {
            const userItem = `<a class="list-group-item user">${data[i]['username']}</a>`;
            $(userItem).appendTo('#user-list');
        }
        $('.user').click(function () {
            groupActive = false
            userList.children('.active').removeClass('active');
            groupList.children('.active').removeClass('active');
            let selected = event.target;
            $(selected).addClass('active');
            setCurrentRecipient(selected.text);
        });
    });
}

function drawMessage(message) {
    let position = 'left';
    const date = new Date(message.timestamp);
    if (message.user === currentUser) position = 'right';
    const messageItem = `
            <li class="message ${position}">
                <div class="avatar">${message.user}</div>
                    <div class="text_wrapper">
                        <div class="text">${message.body}<br>
                            <span class="small">${date}</span>
                    </div>
                </div>
            </li>`;
    $(messageItem).appendTo('#messages');
}

function getConversation(recipient) {
    $.getJSON(`/api/v1/message/?target=${recipient}`, function (data) {
        messageList.children('.message').remove();
        for (let i = data['results'].length - 1; i >= 0; i--) {
            drawMessage(data['results'][i]);
        }
        messageList.animate({ scrollTop: messageList.prop('scrollHeight') });
    });

}

function getMessageById(message) {
    $.getJSON(`/api/v1/message/${id}/`, function (data) {
        if (data.user === currentRecipient ||
            (data.recipient === currentRecipient && data.user == currentUser)) {
            drawMessage(data);
        }
        messageList.animate({ scrollTop: messageList.prop('scrollHeight') });
    });
}

function sendMessage(recipient, body) {
    $.post('/api/v1/message/', {
        recipient: recipient,
        body: body
    }).fail(function () {
        alert('Error! Check console!');
    });
}

function setCurrentRecipient(username) {
    currentRecipient = username;
    getConversation(currentRecipient);
    enableInput();
}


function enableInput() {
    chatInput.prop('disabled', false);
    chatButton.prop('disabled', false);
    chatInput.focus();
}

function disableInput() {
    chatInput.prop('disabled', true);
    chatButton.prop('disabled', true);
}

// Group functions

function updateGroupList() {
    $.getJSON(`api/v1/group/?target=${currentUser}`, function (data) {

        groupList.children('.group').remove();
        for (let i = 0; i < data.length; i++) {
            const groupItem = `<a class="list-group-item group">${data[i]['name']}</a>`;
            $(groupItem).appendTo('#group-list');
        }
        $('.group').click(function () {
            groupActive = true
            groupList.children('.active').removeClass('active');
            userList.children('.active').removeClass('active');
            let selected = event.target;
            $(selected).addClass('active');
            setCurrentGroup(selected.text);
        });
    });
}
function getGroupMessage(id) {
    $.getJSON(`/api/v1/group/message/${id}/`, function (data) {

        if (currentGroup === data.group) {
            drawGroupMessage(data);

        }

        messageList.animate({ scrollTop: messageList.prop('scrollHeight') });
    });
}

function setCurrentGroup(name) {
    currentGroup = name;
    getGroupConversation(currentGroup);
    enableInput();
}
function getGroupConversation(currentGroup) {
    $.getJSON(`/api/v1/group/message/?target=${currentGroup}`, function (data) {
        messageList.children('.message').remove();
        for (let i = data['results'].length - 1; i >= 0; i--) {
            drawGroupMessage(data['results'][i]);
        }
        messageList.animate({ scrollTop: messageList.prop('scrollHeight') });
    });

}

function drawGroupMessage(message) {
    let position = 'left';
    const date = new Date(message.time);
    if (message.sender == currentUser) {
        position = 'right';

    }

    const messageItem = `
            <li class="message ${position}">
                <div class="avatar">${message.sender}</div>
                    <div class="text_wrapper">
                        <div class="text">${message.body}<br>
                            <span class="small">${date}</span>
                    </div>
                </div>
            </li>`;
    $(messageItem).appendTo('#messages');
}

function sendGroupMessage(group, body) {
    $.post('/api/v1/group/message/', {
        group: group,
        body: body
    })
        .fail(function () {
            alert('Error! Check console!');
        });
}

$(document).ready(function () {
    updateUserList();
    updateGroupList()
    disableInput();

    //    let socket = new WebSocket(`ws://127.0.0.1:8000/?session_key=${sessionKey}`);
    var socket = new WebSocket(
        'ws://' + window.location.host +
        '/ws?session_key=${sessionKey}')

    chatInput.keypress(function (e) {
        if (e.keyCode == 13)
            chatButton.click();
    });

    chatButton.click(function () {
        // Sending message to a group
        if (groupActive) {
            if (chatInput.val().length > 0) {
                sendGroupMessage(currentGroup, chatInput.val());
                chatInput.val('');
            }
        }
        //sending message to a chat
        else {
            if (chatInput.val().length > 0) {
                sendMessage(currentRecipient, chatInput.val());
                chatInput.val('');
            }
        }
    });

    socket.onmessage = function (e) {
        message = e.data
        id = JSON.parse(message).message
        group = JSON.parse(message).group
        if (group) {
            getGroupMessage(id)
        }
        else {
            getMessageById(e.data);
        }
    };
});