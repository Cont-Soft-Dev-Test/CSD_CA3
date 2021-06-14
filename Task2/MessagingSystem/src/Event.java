public class Event {

    private String name;
    private int priority;

    // Constructor
    public Event(String name, int priority) {

        this.name = name;
        this.priority = priority;
    }

    // getters (data can only be changed on creating a new event object)
    public String getName() {
        return this.name;
    }

    public int getPriority() {
        return this.priority;
    }
}