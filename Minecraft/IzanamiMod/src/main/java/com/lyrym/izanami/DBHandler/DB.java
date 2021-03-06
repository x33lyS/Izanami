package com.lyrym.izanami.DBHandler;

import com.mysql.cj.jdbc.Driver;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.lang.module.Configuration;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;
import java.util.Properties;



public class DB {
    //JDBC and database properties.
    private static final String DB_DRIVER = "com.mysql.jdbc.Driver";


    public static Connection getConnection(){
        String DB_URL = null;
        String DB_USERNAME = null;
        String DB_PASSWORD = null;
        try(InputStream input = new FileInputStream("config.properties")) {

            Properties prop = new Properties();

            // load a properties file
            prop.load(input);

            DB_URL = prop.getProperty("db.url");
            DB_USERNAME = prop.getProperty("db.user");
            DB_PASSWORD = prop.getProperty("db.password");
        } catch (IOException ex) {
            ex.printStackTrace();
        }
        Connection conn;
        try{
            //Register the JDBC driver
            DriverManager.registerDriver (new Driver());
            //Class.forName(DB_DRIVER);
            System.out.println(DB_URL);
            //Open the connection
            conn = DriverManager.getConnection(DB_URL,DB_USERNAME,DB_PASSWORD);

            if(conn != null){
                System.out.println("Successfully connected.");
            }else{
                System.out.println("Failed to connect.");
            }
        }catch(Exception e){
            e.printStackTrace();
            conn = null;
        }
        return conn;
    }

    public static void UpdateProfile(int scale){
        Connection conn = null ;
        Statement statement = null;

        String query = String.format("UPDATE currentprofile SET profile = 'MINECRAFT', scale = %s",scale);

        try{
            //get connection
            conn = getConnection();

            //create statement
            statement = conn.createStatement();

            //execute query
            statement.executeUpdate(query);

            //close connection
            statement.close();
            conn.close();

            System.out.println("Record inserted successfully.");
        }catch(Exception e){
            e.printStackTrace();
        }
    }
}
