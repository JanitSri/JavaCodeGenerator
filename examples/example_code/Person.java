abstract class Person implements Auth {

	private String name;
	private Address address;
	private String email;

	public String getFullName() {}

	public String getName() {
 		return this.name; 
	}

	public void setName(String name) {
 		this.name = name; 
	}

	public Address getAddress() {
 		return this.address; 
	}

	public void setAddress(Address address) {
 		this.address = address; 
	}

	public String getEmail() {
 		return this.email; 
	}

	public void setEmail(String email) {
 		this.email = email; 
	}

	 public boolean signIn() {
 		// ***requires implementation*** 
	}

	 public boolean signOut() {
 		// ***requires implementation*** 
	}

	 public String validatePassword() {
 		// ***requires implementation*** 
	}

}
