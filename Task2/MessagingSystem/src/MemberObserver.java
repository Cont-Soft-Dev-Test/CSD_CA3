public class MemberObserver implements Observer {

    private String name;
    private int eventID;

    public MemberObserver(String name, int eventID) {

        this.name = name;
        this.eventID = eventID;
    }

    public String getName() {
        return this.name;
    }

    @Override
    public void update(Event event) {

        System.out.println("\nDeveloper's name: " + this.name);
        System.out.println("Event " + event.getName() + " has been triggered!");
    }
}