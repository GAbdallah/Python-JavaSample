package com.wv.app;


import com.wv.app.Employee;
import com.wv.app.DBCPDataSource;
import com.wv.app.PwdHasher;

import org.apache.commons.collections4.MapUtils;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.LambdaLogger;

import java.sql.*;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.util.Map;




/**

 Secure log in using Lambda


*/
public class LambdaMethodHandler implements RequestHandler<Map<String,String>, String>{
    
  Gson gson = new GsonBuilder().setPrettyPrinting().create();
  
  Connection conn;
  
  PwdHasher hasher = new PwdHasher();
   
   
   
   
  public  LambdaMethodHandler() throws Exception{
	  
	  if (conn == null || conn.isClosed()){
		  try{
		  	conn = DBCPDataSource.getConnection();
			
        } catch (SQLException e) {
                 System.err.format("SQL State: %s\n%s", e.getSQLState(), e.getMessage());
        } catch (Exception e) {
                 e.printStackTrace();
        }
    	  
		  
	  	  		
	  }
  	
  }
  
    
    
  @Override
  public String handleRequest(Map<String,String> event, Context context) 
  {
	  
	  String response = new String("400");
	  
	   try {
		   
		   
		   
		    // Check if the connection is closed 
		   
	 	    if ( conn != null && conn.isClosed()) {
		  
	 		  	conn = DBCPDataSource.getConnection();
			
	 	  	}
		  
		  
		  
		  
	 	  String SQL_SELECT = "SELECT U.login as employee_id, E.name_related as first_name, E.last_name, J.name as job_title, RE.emp_no as reporting_manager_id " +
	                         "FROM res_users U " +
	                         "JOIN hr_employee E ON E.emp_no = U.login " +
	                         "JOIN hr_job J ON J.id = E.job_id " +
	                         "LEFT JOIN hr_employee RE ON RE.id = E.reporting_manager " +
	                         "WHERE U.active = 'true' AND U.login =? LIMIT 1";
	  
	 	  PreparedStatement preparedStatement = conn.prepareStatement(SQL_SELECT);
		  
		  
		  // Verify paramters

          if (MapUtils.isEmpty(event) || !event.containsKey("employee_id") 
		  				|| !event.containsKey("password")){
							response = new String("400 error: Invalid paramaters!");
							
							return response;
          	
          }
		  

		  String employee_id = event.get("employee_id");
		  
		  String password = event.get("password");
		  
		  String hasher_pwd = hasher.encode(password,"", 19000);
		  
	 	  preparedStatement.setString(1, employee_id);
		  
		  ResultSet resultSet = preparedStatement.executeQuery();
		  
		  if(resultSet.next()) {
		 	   	
		      				LambdaLogger logger = context.getLogger();
		      				response = new String("200 OK");
			  
			  			  	 // Get Employee details
			 
			                 employee_id = resultSet.getString("employee_id");
			                 String first_name = resultSet.getString("first_name");
			                 String last_name = resultSet.getString("last_name");
			                 String job_title = resultSet.getString("job_title");
							 String reporting_manager_id = resultSet.getString("reporting_manager_id");
							 
			                 Employee obj = new Employee();
			                 obj.setEmployee_id(employee_id);
							 obj.setFirst_name(first_name);
							 obj.setLast_name(last_name);
							 obj.setJob_title(job_title);
							 obj.setReporting_manager_id(reporting_manager_id);
							 
							 logger.log("EVENT: " + gson.toJson(obj));
			                 
		  
		      return hasher_pwd;
		  }
	     
	   
      } catch (SQLException e) {
               System.err.format("SQL State: %s\n%s", e.getSQLState(), e.getMessage());
      } catch (Exception e) {
               e.printStackTrace();
      }
	  
	  return response;

   }
	 
}

