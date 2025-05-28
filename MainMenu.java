import javax.swing.*;
import javax.swing.JFrame;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;

public class MainMenu implements ActionListener {

    JFrame frame = new JFrame();
    private MainMenuPanel mainPanel;
    private JButton button;

    MainMenu() {

        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(1280, 720);
        frame.setTitle("Booru Sort");
        frame.setLocationRelativeTo(null);

        // Set layout explicitly for positioning
        frame.setLayout(new BorderLayout());

        // Left white panel (sidebar)
        mainPanel = new MainMenuPanel();
        mainPanel.addMouseListener(new PopClickListener());


        frame.add(mainPanel, BorderLayout.WEST);

        // Optional center panel (black background)
        JPanel centerPanel = new JPanel();
        centerPanel.setBackground(new Color(32, 32, 32));
        centerPanel.addMouseListener(new PopClickListener());
        centerPanel.setOpaque(true);
        frame.add(centerPanel, BorderLayout.CENTER);

        frame.setVisible(true);



    }


    @Override
    public void actionPerformed(ActionEvent e) {

    }

    static class menuRightClick extends JPopupMenu {

        JMenuItem folder;
        JMenuItem tag;

        boolean isTagClicked = false;
        static CreateTag currentTagWindow = null;

        public menuRightClick(Point location, MainMenuPanel panelParam) {

            folder = new JMenuItem("New folder");
            folder.addActionListener(e -> {

            });
            add(folder);


            //tag
            tag = new JMenuItem("New tag");
            tag.addActionListener(e -> {
                isTagClicked = true;

                if (currentTagWindow != null) {
                    currentTagWindow.close();
                }

                currentTagWindow = new CreateTag(location, panelParam);
            });
            add(tag);
        }

        public boolean isTagClicked() {
            return isTagClicked;
        }
    }

    class PopClickListener extends MouseAdapter {
        public void mousePressed(MouseEvent e) {
            if (e.isPopupTrigger())
                doPop(e);
        }

        public void mouseReleased(MouseEvent e) {
            if (e.isPopupTrigger())
                doPop(e);
        }

        private void doPop(MouseEvent e) {
            Point screenLoc = e.getLocationOnScreen();
            MainMenu.menuRightClick menu = new MainMenu.menuRightClick(screenLoc, mainPanel);

            menu.show(e.getComponent(), e.getX(), e.getY());
        }
    }

}
