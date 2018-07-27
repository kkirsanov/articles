void init()
{
  omniDrive.setComId( com.id() );
  // Connect
  com.setAddress( "127.0.0.1" );
  com.connect();
  std::cout << std::endl << "Connected" << std::endl;
}
