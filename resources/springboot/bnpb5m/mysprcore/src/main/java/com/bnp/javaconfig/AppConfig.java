package com.bnp.javaconfig;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Scope;

@Configuration
public class AppConfig {

	@Bean(name = "gs1")
	@Scope("prototype")
	public GreetingServiceImpl getGs1() {
		GreetingServiceImpl gs = new GreetingServiceImpl();
		gs.setGreeting("Good Afternoon");
		return gs;
	}

	@Bean(name = "gs2")
	public GreetingServiceImpl getGs2() {
		GreetingServiceImpl gs = new GreetingServiceImpl("Good Evening");
		return gs;
	}
}
