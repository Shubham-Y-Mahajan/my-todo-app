package com.bnp.javaconfig;

public class GreetingServiceImpl implements GreetingService {

	private String greeting;

	public GreetingServiceImpl() {
		super();
		// TODO Auto-generated constructor stub
	}

	public GreetingServiceImpl(String greeting) {
		super();
		this.greeting = greeting;
	}

	public String getGreeting() {
		return greeting;
	}

	public void setGreeting(String greeting) {
		this.greeting = greeting;
	}

	@Override
	public void sayHello() {
		System.out.println("Hello " + greeting);

	}

}
