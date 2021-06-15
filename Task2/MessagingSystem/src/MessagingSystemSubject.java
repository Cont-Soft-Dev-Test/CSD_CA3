import java.util.ArrayList;
import java.util.List;

public class MessagingSystemSubject implements Subject {

    private final List<Observer> observerList;
    private final List<Event> eventList;

    private final Object MUTEX = new Object();

    public MessagingSystemSubject() {

        this.observerList = new ArrayList<>();
        this.eventList = new ArrayList<>();
    }

    public List<Event> getEventList() {
        return eventList;
    }

    @Override
    public void register(Observer observer) {
        if (observer == null) {
            throw new NullPointerException("Null Observer");
        }

        synchronized (MUTEX) {
            if (!this.observerList.contains(observer)) {
                this.observerList.add(observer);
            }
        }
    }

    @Override
    public void unregister(Observer observer) {

        synchronized (MUTEX) {
            this.observerList.remove(observer);
        }
    }

    @Override
    public void notifyObservers(int eventListIndex) {

        boolean notified = false;
        List<Observer> localObserverList;

        synchronized (MUTEX) {

            localObserverList = new ArrayList<>(this.observerList);
        }

        System.out.println("\n==================");
        System.out.println("Notification sent!");
        System.out.println("==================");

        for (Observer observer : localObserverList) {

            if (this.eventList.get(eventListIndex) == observer.getEvent()) {
                observer.update();
                notified = true;
            }
        }

        if (!notified) {
            System.out.println("\nEvent " + this.eventList.get(eventListIndex).getName() + ":");
            System.out.println("Nobody was registered to this event!");
        }
    }
}