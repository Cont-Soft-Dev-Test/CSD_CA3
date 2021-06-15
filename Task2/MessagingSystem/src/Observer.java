public interface Observer {

    String getName();
    int getEventID();
    void update(Event event);
}