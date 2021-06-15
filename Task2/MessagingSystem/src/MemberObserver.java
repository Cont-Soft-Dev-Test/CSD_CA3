public class MemberObserver implements Observer {

    private String name;
    private int eventID;

    public MemberObserver(String name, int eventID) {

        this.name = name;
        this.eventID = eventID;
    }

    @Override
    public String getName() {
        return this.name;
    }

    @Override
    public int getEventID() {
        return eventID;
    }

    @Override
    public void update(Event event) {

        System.out.println("\nDeveloper to be alerted: " + this.name);
        System.out.println("Event " + event.getName() + " has been triggered!");
    }
}