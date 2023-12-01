css = '''

<style>
.chat_messages {
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
}

.chat_message.user{
    background-color: #2b313e;
}

.chat_message.bot{
    background-color: #475063;
}

.chat_message .message{
    width: 85%;
    padding: 0 1.5rem;
    color: #fff
}

</style>

'''

bot_templete = '''

<div class="chat_message bot">
    <div class="message">{{msg}}</div>
</div>

'''
user_templete = '''

<div class="chat_message user">
    <div class="message">{{msg}}</div>
</div>

'''