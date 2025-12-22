// Quick server test
try {
    console.log('Testing server startup...');
    require('./server.js');
} catch (error) {
    console.error('Server error:', error.message);
    console.error('Stack:', error.stack);
}
