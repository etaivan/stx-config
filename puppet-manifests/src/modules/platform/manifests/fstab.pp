class platform::fstab {
  include ::platform::params

  if $::personality != 'controller' {
    exec { 'Unmount NFS filesystems':
      command => 'umount -a -t nfs ; sleep 5 ;',
    } ->
    mount { '/opt/platform':
      device   => 'controller-platform-nfs:/opt/platform',
      fstype   => 'nfs',
      ensure   => 'present',
      options  => "${::platform::params::nfs_mount_options},_netdev",
      atboot   => 'yes',
      remounts => true,
    } ->
    exec { 'Remount NFS filesystems':
      command => 'umount -a -t nfs ; sleep 1 ; mount -a -t nfs',
    }
  }
}
