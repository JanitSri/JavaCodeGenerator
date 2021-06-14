public class Bank {

	private int bankId;
	private String name;
	private String address;
	private Teller[] tellers;
	private Customer[] customers;

	public int getBankId() {
 		return this.bankId; 
	}

	public void setBankId(int bankId) {
 		this.bankId = bankId; 
	}

	public String getName() {
 		return this.name; 
	}

	public void setName(String name) {
 		this.name = name; 
	}

	public String getAddress() {
 		return this.address; 
	}

	public void setAddress(String address) {
 		this.address = address; 
	}

	public Teller[] getTellers() {
 		return this.tellers; 
	}

	public void setTellers(Teller[] tellers) {
 		this.tellers = tellers; 
	}

	public Customer[] getCustomers() {
 		return this.customers; 
	}

	public void setCustomers(Customer[] customers) {
 		this.customers = customers; 
	}

}
