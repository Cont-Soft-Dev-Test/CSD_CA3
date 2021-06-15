import java.util.ArrayList;
import java.util.List;

public class MessagingSystemSubject implements Subject {

    private final List<Observer> observerList;
    private final List<Event> eventList;

    // a MUTEX object to ensure the safe multi-threaded processes
    private final Object MUTEX = new Object();

    // Constructor
    public MessagingSystemSubject() {

        this.observerList = new ArrayList<>();
        this.eventList = new ArrayList<>();
    }

    // getter
    public List<Event> getEventList() {
        return eventList;
    }

    // A method to register the observer
    @Override
    public void register(Observer observer) {

        // test if the observer object is valid
        if (observer == null) {
            throw new NullPointerException("Null Observer");
        }

        // apply lock
        synchronized (MUTEX) {

            // test if the observer is already on the list
            if (!this.observerList.contains(observer)) {

                // add the observer to the list
                this.observerList.add(observer);
            }
        }
    }

    // A method to remove the observer from the list
    @Override
    public void unregister(Observer observer) {

        // apply lock
        synchronized (MUTEX) {

            // remove the observer from the list
            this.observerList.remove(observer);
        }
    }

    // This method sends the notification when the given event is triggered
    @Override
    public void notifyObservers(int eventListIndex) {

        boolean notified = false;
        List<Observer> localObserverList;

        // apply the lock
        synchronized (MUTEX) {

            // get a local copy of the observer list to prevent the changes in multi-threaded environment
            localObserverList = new ArrayList<>(this.observerList);
        }

        // feedback
        System.out.println("\n==================");
        System.out.println("Notification sent!");
        System.out.println("==================");

        // iterate through the observer list
        for (Observer observer : localObserverList) {

            // if the observer is subscribed for the event
            if (this.eventList.get(eventListIndex) == observer.getEvent()) {

                // update the selected observers
                observer.update();
                notified = true;
            }
        }

        // if nobody subscribed for the given event
        if (!notified) {

            // send feedback about it
            System.out.println("\nEvent " + this.eventList.get(eventListIndex).getName() + ":");
            System.out.println("Nobody was registered to this event!");
        }
    }
}