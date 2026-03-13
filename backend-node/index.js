const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const cors = require('cors');

const app = express();
app.use(cors());

const server = http.createServer(app);
// Allow your Vercel frontend to connect without CORS errors
const io = new Server(server, {
    cors: { origin: "*" }
});

io.on('connection', (socket) => {
    console.log('A client connected:', socket.id);

    // Listen for a PO update event
    socket.on('po_status_change', (data) => {
        console.log("Status changed:", data);
        // Broadcast a real-time notification to EVERY connected screen
        io.emit('notification', `Real-Time Alert: PO #${data.reference} was submitted successfully!`);
    });

    socket.on('disconnect', () => {
        console.log('Client disconnected');
    });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`Node.js Real-Time Server running on port ${PORT}`);
});