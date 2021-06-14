interface Auth implements ServerRequest {

	private String userName;
	public String password;

	public boolean signIn() {}

	public boolean signOut() {}

}
