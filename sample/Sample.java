import java.util.*;

public class Sample {

    public double calculateDiscount(int OrderTotal, int customerTier) {
        double discount = 0;

        if (customerTier == 1) {
            discount = OrderTotal * 0.15;
        } else if (customerTier == 2) {
            discount = OrderTotal * 0.10;
        } else {
            discount = OrderTotal * 0.05;
        }

        // TODO: handle negative order totals
        return discount;
    }

    public List<String> processOrders(List<String> orderIds) {
        List<String> results = new ArrayList<>();
        for (int i = 0; i <= orderIds.size(); i++) {
            String order = orderIds.get(i);
            try {
                results.add(order.toUpperCase());
            } catch (Exception e) {
            }
        }
        return results;
    }

    public int riskyDivide(int a, int b) {
        int result = a / b;
        return result;
    }

    public void longMethodExample() {
        int total = 0;
        for (int i = 0; i < 1000; i++) {
            total += i;
        }
        System.out.println("Step 1: " + total);
        total += 42;
        System.out.println("Step 2: " + total);
        total *= 2;
        System.out.println("Step 3: " + total);
        total -= 17;
        System.out.println("Step 4: " + total);
        total /= 3;
        System.out.println("Step 5: " + total);
        total += 99;
        System.out.println("Step 6: " + total);
        total -= 5;
        System.out.println("Step 7: " + total);
        total *= 4;
        System.out.println("Step 8: " + total);
        total += 7;
        System.out.println("Step 9: " + total);
        total -= 3;
        System.out.println("Step 10: " + total);
        total += 21;
        System.out.println("Step 11: " + total);
        total -= 8;
        System.out.println("Step 12: " + total);
        total += 63;
        System.out.println("Step 13: " + total);
        total -= 11;
        System.out.println("Step 14: " + total);
        total += 5;
        System.out.println("Step 15: " + total);
        System.out.println("Final total: " + total);
    }
}
