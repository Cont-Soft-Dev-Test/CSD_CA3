public class MemberObserver implements Observer {

    private final String name;
    private final Event event;


    // Constructor
    public MemberObserver(String name, Event event) {

        this.name = name;
        this.event = event;
    }

    // getter
    @Override
    public Event getEvent() {
        return this.event;
    }

    // The update method updates the corresponding observers about the triggered event
    @Override
    public void update() {

        System.out.println("\nDeveloper to be alerted: " + this.name);
        System.out.println("Event " + this.event.getName() + " has been triggered!");
        System.out.println("Event priority: " + this.event.getPriority());
    }
}