public class MessagingSystemRunner {
    public static void main(String[] args) {

        // create messaging system
        MessagingSystemSubject messagingSystem = new MessagingSystemSubject();
        System.out.println("Messaging System created!");

        // add events to the event list
        messagingSystem.getEventList().add(new Event("Code checked in", 5));
        messagingSystem.getEventList().add(new Event("Code pushed", 5));
        messagingSystem.getEventList().add(new Event("Build completed", 2));
        messagingSystem.getEventList().add(new Event("Build failed", -2));
        messagingSystem.getEventList().add(new Event("Test failed", -1));
        messagingSystem.getEventList().add(new Event("Test passed", 3));
        messagingSystem.getEventList().add(new Event("Release deployment passed", 1));
        System.out.println("Event list created!");

        // create observers
        Observer observer1 = new MemberObserver("Dave", messagingSystem.getEventList().get(6));
        Observer observer2 = new MemberObserver("John", messagingSystem.getEventList().get(2));
        Observer observer3 = new MemberObserver("Anna", messagingSystem.getEventList().get(2));
        Observer observer4 = new MemberObserver("Cathal", messagingSystem.getEventList().get(5));
        Observer observer5 = new MemberObserver("Aiofe", messagingSystem.getEventList().get(6));
        System.out.println("Observers created!");

        // register observers
        messagingSystem.register(observer1);
        messagingSystem.register(observer2);
        messagingSystem.register(observer3);
        messagingSystem.register(observer4);
        messagingSystem.register(observer5);
        System.out.println("Observers registered!");

        // Notify observers
        messagingSystem.notifyObservers(2);
        messagingSystem.notifyObservers(6);
        messagingSystem.notifyObservers(0);
    }
}
