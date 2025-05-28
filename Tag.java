import java.util.HashSet;

public class Tag {
    private HashSet<String> tags = new HashSet<>();

    public Tag() {
        tags = new HashSet<>();
    }

    public void add(String tagName) {
        tags.add(tagName);
    }

}
