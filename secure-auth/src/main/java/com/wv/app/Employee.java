package com.wv.app;

import java.math.BigDecimal;
import java.time.LocalDateTime;











/***
    Employee DTO Object 

*/

public class Employee {

    private String employee_id;
    private String first_name;
    private String last_name;
	private String job_title;
    private String reporting_manager_id;
	
	
	
	// Getter
	  public String getEmployee_id() {
	    return employee_id;
	  }




	  // Setter
	  public void setEmployee_id(String employee_id) {
	    this.employee_id = employee_id;
	  }
	  
	  
  	// Getter
  	  public String getFirst_name() {
  	    return first_name;
  	  }
	  
	  
	  
	  

  	  // Setter
  	  public void setFirst_name(String first_name) {
  	       this.first_name = first_name;
  	  }
	  
	  
	  
	  
	  
  	// Getter
  	  public String getLast_name() {
  	    return last_name;
  	  }





  	  // Setter
  	  public void setLast_name(String last_name) {
  	    this.last_name = last_name;
  	  }
	  
	  
	  
	  
	  
    // Getter
    	  public String getJob_title() {
    	    return job_title;
    	  }





    	  // Setter
    	  public void setJob_title(String job_title) {
    	    this.job_title = job_title;
    	  }
	  
	  
	  
	  
    // Getter
      public String getReporting_manager_id() {
    	    return reporting_manager_id;
      }
	  
	  
	  
	  

     // Setter
     public void setReporting_manager_id(String reporting_manager_id) {
    	    this.reporting_manager_id = reporting_manager_id;
    }
	
	
	  

    
}