import javax.swing.*;
import java.awt.*;

public class MainMenuPanel extends JPanel {

    public MainMenuPanel() {

        setPreferredSize(new Dimension(200, 360));
        setBackground(new Color(64, 64, 64));

        setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));

        setOpaque(true);

    }

    public void addTagButton(String tagInput) {
        JButton newButton = new JButton(tagInput);

        newButton.setMaximumSize(new Dimension(200, 25));
        newButton.setBackground(new Color(128,128,128 ));
        newButton.setAlignmentX(Component.CENTER_ALIGNMENT);

        if (getComponentCount() == 0) {
            add(Box.createVerticalGlue());
        }

        int buttonSpacing = 8;
        add(Box.createVerticalStrut(buttonSpacing));


        add(newButton);
        revalidate();
        repaint();
    }
}