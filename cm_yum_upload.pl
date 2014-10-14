#!/usr/bin/perl


# Author: Ronan Cunningham
#  
# Script used in conjunction with yum_upload.sh to add files to and update a yum repo
# on the server where the script runs.
#
# - Apache requires the webdav and cgi modules
# 
# - Assumes Apache is setup with the cgi folder named 'cm' 
# and this script is named 'cm_yum_upload.pl'
#
# - yum_upload.sh assumes the webdav folder is named 'webdav'. Add the actual location
# to  %build_server_data
#
# - Apache user requires access to move files from the webdav folder to the repo dir
# and permission to run 'createrepo --update ...' command
#
#
#


use strict;
use warnings;
use Sys::Hostname;
use File::Copy;
use File::Temp qw(tempdir);
use CGI qw(:standard);

$SIG{__DIE__} = sub { print @_, "\n"; exit 255 };

print "Content-type: text/html\n\n";

my $tmp_dir = tempdir( CLEANUP => 1 );
my $host = hostname;
my $query = new CGI;


my %build_server_data = (

		'sl73nyumapq001' =>
                        { 'repo_mount_pt'  => '/rpm-repo',
                           'repo_dir'      => '/rpm-repo/cmrepo/',
                           'webdav_dir'    => "/var/www/html/webdav/"},
		'sl73nyumapq002' =>
                        { 'repo_mount_pt'  => '/rpm-repo',
                           'repo_dir'      => '/rpm-repo/devrepo/',
                           'webdav_dir'    => "/var/www/html/webdav/"},
                'sl73nyumapq003' =>
                        { 'repo_mount_pt'  => '/rpm-repo',
                          'repo_dir'      => '/rpm-repo/infrarepo/',
                          'webdav_dir'    => "/var/www/html/webdav/"},
                'sl73nyumapq004' =>
                        { 'repo_mount_pt'  => '/rpm-repo',
                          'repo_dir'      => '/rpm-repo/3rdparty/',
                          'webdav_dir'    => "/var/www/html/webdav/"},
                        );

my $mnt_pt        = $build_server_data{$host}{repo_mount_pt};
my $webdav_dir    = $build_server_data{$host}{webdav_dir};
my $repo_dir      = $build_server_data{$host}{repo_dir};

if (defined $query->param('update_repo')) {
    my $update_repo = `createrepo -s sha --update $repo_dir`;
    print $?;
						
}

if (defined $query->param('repo_mount')) {		
	my $mnt             = check_exists ($mnt_pt, 'dir');
	my $available_space = check_mount_space ($mnt);
	print $available_space;
						
}

if (defined $query->param('move_to_repo')) {		
	my $file          = $query->param('move_to_repo');
	my $transfer_dir  = $query->param('transfer_dir');
	my $full_path     = "${webdav_dir}" . "$transfer_dir" . '/' . "${file}";
	my $new_path      = "$repo_dir" . "$file";

	move($full_path, $new_path) or die "\nCound not copy $full_path to $new_path :\n $!";
	print $file;
								
}


if (defined $query->param('cksum')) {
	
	my $file          = $query->param('cksum');
	my $transfer_dir  = $query->param('transfer_dir');
	my $full_path     = "${webdav_dir}" . "$transfer_dir" . '/' . "${file}";
	my $file_to_check = check_exists ($full_path , 'file');
	my $cksum         = cksum ($file_to_check);
	print $cksum;
				
}


sub check_exists {
	
	my $item_to_check = shift;
	my $item_type     = shift;
	
	# Check Directory
	if ( "$item_type" eq 'dir' &&  ! -d "$item_to_check" ) {
		die "$item_to_check not found on $host :\n $!"; 
	
	}
	 elsif ( "$item_type" eq 'dir' && -d "$item_to_check" ){
	 	return $item_to_check;
	 }
	# Check file
	if ( "$item_type" eq 'file' &&  ! -e "$item_to_check" ) {
		die "$item_to_check not found on $host :\n $!"; 
		
	}
	 elsif ( "$item_type" eq 'file' && -e "$item_to_check" ){
	 	return $item_to_check;
	 }	
}

sub cksum {
	
	my $file_to_cksum = shift;
	my $cksum = `cksum $file_to_cksum  | cut -d\\  -f 1`;
	return $cksum;		
}

#sudo   createrepo --update /tmp/repos/yumrrepo


sub check_mount_space {
	my $mnt_to_check = shift;
	
	my @disk_space      = `df $mnt_to_check`;
	my $mount_info      = $disk_space[2];
	my @mount_info      = split (/ +/,$mount_info);
	my $available_space = "$mount_info[3]\n";
	return $available_space;
}	
