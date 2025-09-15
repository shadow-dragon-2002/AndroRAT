package com.example.reverseshell2;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;

/**
 * Fake Help activity for evasion
 */
public class HelpActivity extends Activity {
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        TextView textView = new TextView(this);
        textView.setText("Help & Support\n\n" +
                "Frequently Asked Questions:\n\n" +
                "Q: How does the app optimize my device?\n" +
                "A: The app manages background processes and clears unnecessary cache.\n\n" +
                "Q: Is my data safe?\n" +
                "A: Yes, we follow strict privacy guidelines and do not collect personal data.\n\n" +
                "Q: How often should I run optimization?\n" +
                "A: We recommend daily optimization for best performance.\n\n" +
                "For technical support, contact: support@techsoft-solutions.com");
        textView.setPadding(40, 40, 40, 40);
        textView.setTextSize(14);
        
        setContentView(textView);
    }
}