311,318d310
< 	      if ((flags & SEVAL_FUNCDEF) && command->type != cm_function_def)
< 		{
< 		  internal_warning ("%s: ignoring function definition attempt", from_file);
< 		  should_jump_to_top_level = 0;
< 		  last_result = last_command_exit_value = EX_BADUSAGE;
< 		  break;
< 		}
< 
379,381d370
< 
< 	      if (flags & SEVAL_ONECMD)
< 		break;
