public class Customer extends Person {

	private String address;
	private String phoneNum;
	private int accountNum;

	public boolean generalInquiry() {}

	public boolean depositMoney() {}

	public boolean withdrawMoney() {}

	public Account openAccount() {}

	public Account closeAccount() {}

	public boolean applyForLoan() {}

	public boolean requestCard() {}

	public String getAddress() {
 		return this.address; 
	}

	public void setAddress(String address) {
 		this.address = address; 
	}

	public String getPhoneNum() {
 		return this.phoneNum; 
	}

	public void setPhoneNum(String phoneNum) {
 		this.phoneNum = phoneNum; 
	}

	public int getAccountNum() {
 		return this.accountNum; 
	}

	public void setAccountNum(int accountNum) {
 		this.accountNum = accountNum; 
	}

}
