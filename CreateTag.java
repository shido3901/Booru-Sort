import javax.swing.*;
import java.awt.*;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;

public class CreateTag {
    public final JDialog dialog;

    public CreateTag(Point location, MainMenuPanel panel) {
        dialog = new JDialog(); // Use JDialog instead of JWindow
        dialog.setUndecorated(true); // Makes it look like a popup
        dialog.setSize(120, 80);
        dialog.setLayout(new BorderLayout());
        dialog.setAlwaysOnTop(true);

        int x = location.x;
        int y = location.y - dialog.getHeight(); // Align bottom-left
        dialog.setLocation(x, y);

        // Input panel
        JPanel tagCreate = new JPanel();
        tagCreate.add(new JLabel("Tag name:"));

        JTextField textField = new JTextField(10);
        tagCreate.add(textField);

        textField.addKeyListener(new KeyAdapter() {
            @Override
            public void keyPressed(KeyEvent e) {
                if (e.getKeyCode() == KeyEvent.VK_ENTER) {
                    // Get text entered
                    String tagInput = textField.getText();

                    System.out.println("Tag: " + tagInput);

                    Tag tagName = new Tag();
                    tagName.add(tagInput);
                    panel.addTagButton(tagInput);


                    //Check the hashset in Tag.java
                    // if (tagInput.equals("output")) {
                    //    System.out.println(tagName);
                    //}

                    dialog.dispose();
                }
            }
        });

        // Close button
        JButton close = new JButton("cancel");
        close.setPreferredSize(new Dimension(40, 25));
        close.addActionListener(e -> {
            dialog.dispose();
        });

        dialog.add(tagCreate, BorderLayout.CENTER);
        dialog.add(close, BorderLayout.SOUTH);

        dialog.setFocusableWindowState(true);
        dialog.setVisible(true);
        textField.requestFocusInWindow();
    }

    public void close() {
        dialog.dispose();
    }
}
