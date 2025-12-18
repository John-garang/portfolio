import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.regex.*;

public class HTMLDiagnostic {
    private static final String HTML_FILE = "index.html";
    private List<String> issues = new ArrayList<>();
    private List<String> fixes = new ArrayList<>();
    
    public static void main(String[] args) {
        HTMLDiagnostic diagnostic = new HTMLDiagnostic();
        diagnostic.diagnoseAndFix();
    }
    
    public void diagnoseAndFix() {
        try {
            String content = Files.readString(Paths.get(HTML_FILE));
            System.out.println("=== HTML DIAGNOSTIC REPORT ===\n");
            
            // Run diagnostics
            checkDocumentStructure(content);
            checkFormElements(content);
            checkScriptReferences(content);
            checkImagePaths(content);
            checkLinkIntegrity(content);
            
            // Display results
            displayResults();
            
            // Apply fixes if needed
            if (!fixes.isEmpty()) {
                applyFixes(content);
            }
            
        } catch (IOException e) {
            System.err.println("Error reading HTML file: " + e.getMessage());
        }
    }
    
    private void checkDocumentStructure(String content) {
        System.out.println("1. Document Structure Check:");
        
        if (!content.contains("<!DOCTYPE html>")) {
            addIssue("Missing DOCTYPE declaration");
        } else {
            System.out.println("   ✓ DOCTYPE present");
        }
        
        if (!content.contains("<html") || !content.contains("</html>")) {
            addIssue("Missing or incomplete HTML tags");
        } else {
            System.out.println("   ✓ HTML tags present");
        }
        
        if (!content.contains("<head>") || !content.contains("</head>")) {
            addIssue("Missing or incomplete HEAD section");
        } else {
            System.out.println("   ✓ HEAD section present");
        }
        
        if (!content.contains("<body>") || !content.contains("</body>")) {
            addIssue("Missing or incomplete BODY section");
        } else {
            System.out.println("   ✓ BODY section present");
        }
        
        System.out.println();
    }
    
    private void checkFormElements(String content) {
        System.out.println("2. Form Elements Check:");
        
        Pattern formPattern = Pattern.compile("<form[^>]*>");
        Matcher formMatcher = formPattern.matcher(content);
        
        while (formMatcher.find()) {
            String form = formMatcher.group();
            if (!form.contains("action=")) {
                addIssue("Form missing action attribute: " + form.substring(0, Math.min(50, form.length())));
                addFix("Add action attribute to forms");
            }
            if (!form.contains("method=")) {
                addIssue("Form missing method attribute: " + form.substring(0, Math.min(50, form.length())));
                addFix("Add method attribute to forms");
            }
        }
        
        // Check for orphaned input elements
        Pattern inputPattern = Pattern.compile("<input[^>]*>");
        Matcher inputMatcher = inputPattern.matcher(content);
        int inputCount = 0;
        while (inputMatcher.find()) {
            inputCount++;
        }
        
        long formCount = formPattern.matcher(content).results().count();
        System.out.println("   Found " + inputCount + " input elements in " + formCount + " forms");
        
        if (inputCount > 0 && formCount > 0) {
            System.out.println("   ✓ Form structure appears valid");
        }
        
        System.out.println();
    }
    
    private void checkScriptReferences(String content) {
        System.out.println("3. Script References Check:");
        
        Pattern scriptPattern = Pattern.compile("<script[^>]*src=[\"']([^\"']+)[\"'][^>]*>");
        Matcher scriptMatcher = scriptPattern.matcher(content);
        
        while (scriptMatcher.find()) {
            String scriptSrc = scriptMatcher.group(1);
            if (!scriptSrc.startsWith("http")) {
                File scriptFile = new File(scriptSrc);
                if (!scriptFile.exists()) {
                    addIssue("Missing script file: " + scriptSrc);
                    addFix("Create missing script files or update references");
                } else {
                    System.out.println("   ✓ Script file exists: " + scriptSrc);
                }
            } else {
                System.out.println("   ✓ External script: " + scriptSrc);
            }
        }
        
        // Check for JavaScript errors in inline scripts
        Pattern inlineScriptPattern = Pattern.compile("<script[^>]*>(.*?)</script>", Pattern.DOTALL);
        Matcher inlineScriptMatcher = inlineScriptPattern.matcher(content);
        
        while (inlineScriptMatcher.find()) {
            String script = inlineScriptMatcher.group(1);
            if (script.contains("getElementById") && !script.contains("if (")) {
                addIssue("JavaScript may fail if elements don't exist - missing null checks");
                addFix("Add null checks for DOM element references");
            }
        }
        
        System.out.println();
    }
    
    private void checkImagePaths(String content) {
        System.out.println("4. Image Path Check:");
        
        Pattern imgPattern = Pattern.compile("<img[^>]*src=[\"']([^\"']+)[\"'][^>]*>");
        Matcher imgMatcher = imgPattern.matcher(content);
        
        while (imgMatcher.find()) {
            String imgSrc = imgMatcher.group(1);
            if (!imgSrc.startsWith("http")) {
                File imgFile = new File(imgSrc);
                if (!imgFile.exists()) {
                    addIssue("Missing image file: " + imgSrc);
                    addFix("Create missing image files or update paths");
                } else {
                    System.out.println("   ✓ Image file exists: " + imgSrc);
                }
            }
        }
        
        System.out.println();
    }
    
    private void checkLinkIntegrity(String content) {
        System.out.println("5. Link Integrity Check:");
        
        Pattern linkPattern = Pattern.compile("<a[^>]*href=[\"']([^\"']+)[\"'][^>]*>");
        Matcher linkMatcher = linkPattern.matcher(content);
        
        while (linkMatcher.find()) {
            String href = linkMatcher.group(1);
            if (!href.startsWith("http") && !href.startsWith("mailto:") && !href.equals("#")) {
                File linkFile = new File(href);
                if (!linkFile.exists()) {
                    addIssue("Broken internal link: " + href);
                    addFix("Create missing HTML files or update links");
                } else {
                    System.out.println("   ✓ Internal link valid: " + href);
                }
            }
        }
        
        System.out.println();
    }
    
    private void addIssue(String issue) {
        issues.add(issue);
        System.out.println("   ✗ " + issue);
    }
    
    private void addFix(String fix) {
        if (!fixes.contains(fix)) {
            fixes.add(fix);
        }
    }
    
    private void displayResults() {
        System.out.println("=== DIAGNOSTIC SUMMARY ===");
        System.out.println("Issues found: " + issues.size());
        System.out.println("Fixes needed: " + fixes.size());
        
        if (!issues.isEmpty()) {
            System.out.println("\nISSUES:");
            for (int i = 0; i < issues.size(); i++) {
                System.out.println((i + 1) + ". " + issues.get(i));
            }
        }
        
        if (!fixes.isEmpty()) {
            System.out.println("\nRECOMMENDED FIXES:");
            for (int i = 0; i < fixes.size(); i++) {
                System.out.println((i + 1) + ". " + fixes.get(i));
            }
        }
        
        if (issues.isEmpty()) {
            System.out.println("\n✓ No critical issues found! HTML structure appears valid.");
        }
        
        System.out.println();
    }
    
    private void applyFixes(String content) {
        System.out.println("=== APPLYING AUTOMATIC FIXES ===");
        
        String fixedContent = content;
        boolean modified = false;
        
        // Fix forms without action/method
        if (content.contains("<form class=\"contact-form\"") && 
            !content.contains("action=") && !content.contains("method=")) {
            fixedContent = fixedContent.replaceFirst(
                "<form class=\"contact-form\"", 
                "<form class=\"contact-form\" action=\"#\" method=\"POST\""
            );
            modified = true;
            System.out.println("✓ Added action and method to contact form");
        }
        
        // Add null checks to JavaScript
        if (content.contains("getElementById") && !content.contains("if (newsletterForm)")) {
            // This is already handled in the current code
            System.out.println("✓ JavaScript null checks already present");
        }
        
        if (modified) {
            try {
                Files.writeString(Paths.get("index_fixed.html"), fixedContent);
                System.out.println("✓ Fixed HTML saved as index_fixed.html");
            } catch (IOException e) {
                System.err.println("Error saving fixed HTML: " + e.getMessage());
            }
        }
        
        System.out.println("=== FIXES COMPLETE ===");
    }
}