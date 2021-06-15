import java.util.ArrayList;
import java.util.List;

public class MessagingSystemSubject implements Subject {

    private List<Observer> observerList;
    private List<Event> eventList;

    public MessagingSystemSubject() {

        this.observerList = new ArrayList<>();
        this.eventList = new ArrayList<>();
    }

    public List<Observer> getObserverList() {
        return observerList;
    }

    public List<Event> getEventList() {
        return eventList;
    }

    @Override
    public void register(Observer observer) {
        this.observerList.add(observer);
    }

    @Override
    public void unregister(Observer observer) {
        this.observerList.remove(observer);
    }

    @Override
    public void notifyObservers(int eventID) {
        for (Observer observer : observerList) {

            if (eventID == observer.getEventID()) {

                observer.update(eventList.get(eventID));
            }
        }
    }
}