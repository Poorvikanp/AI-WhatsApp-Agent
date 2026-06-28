const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');

const client = new Client({
    authStrategy: new LocalAuth()
});

// Show QR code to scan
client.on('qr', (qr) => {
    console.log('📱 Scan this QR code with your WhatsApp:');
    qrcode.generate(qr, { small: true });
});

// When connected
client.on('ready', () => {
    console.log('✅ WhatsApp connected and ready!');
});

// When message received
client.on('message', async (msg) => {
    // Ignore status broadcasts
    if (msg.from === 'status@broadcast') return;
    // Ignore empty messages
    if (!msg.body || msg.body.trim() === '') return;
    // Ignore group messages
    if (msg.from.endsWith('@g.us')) return;

    // Get sender name
    const contact = await msg.getContact();
    const senderName = contact.pushname || contact.name || msg.from;

    console.log(`📩 Message from ${senderName}: ${msg.body}`);

    try {
        const response = await fetch('http://127.0.0.1:8000/classify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                from: msg.from,
                sender_name: senderName,
                message: msg.body
            })
        });

        const data = await response.json();

        if (data.reply) {
            await msg.reply(data.reply);
            console.log(`✅ Replied to ${senderName}`);
        } else if (data.escalate) {
            console.log(`🚨 Escalated to Sumit Sir`);
        } else {
            console.log(`🗑️ Spam ignored`);
        }

    } catch (err) {
        console.error('❌ Error:', err.message);
    }
});

// Poll for pending alerts every 5 seconds
setInterval(async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/pending-alerts');
        const data = await response.json();

        if (data.alerts && data.alerts.length > 0) {
            for (const alert of data.alerts) {
                await client.sendMessage(alert.to, alert.message);
                console.log(`🚨 Alert sent to Sumit Sir!`);
            }
        }
    } catch (err) {
        // Silent fail
    }
}, 5000);

client.initialize();