361,365c361,367
< 	  /* Don't import function names that are invalid identifiers from the
< 	     environment, though we still allow them to be defined as shell
< 	     variables. */
< 	  if (legal_identifier (name))
< 	    parse_and_execute (temp_string, name, SEVAL_NONINT|SEVAL_NOHIST|SEVAL_FUNCDEF|SEVAL_ONECMD);
---
> 	  if (posixly_correct == 0 || legal_identifier (name))
> 	    parse_and_execute (temp_string, name, SEVAL_NONINT|SEVAL_NOHIST);
> 
> 	  /* Ancient backwards compatibility.  Old versions of bash exported
> 	     functions like name()=() {...} */
> 	  if (name[char_index - 1] == ')' && name[char_index - 2] == '(')
> 	    name[char_index - 2] = '\0';
381a384,387
> 
> 	  /* ( */
> 	  if (name[char_index - 1] == ')' && name[char_index - 2] == '\0')
> 	    name[char_index - 2] = '(';		/* ) */
