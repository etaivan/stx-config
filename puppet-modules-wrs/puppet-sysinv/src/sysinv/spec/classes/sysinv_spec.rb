#
# Files in this package are licensed under Apache; see LICENSE file.
#
# Copyright (c) 2013-2016 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#
#  Aug 2016: rebase mitaka
#  Jun 2016: rebase centos
#  Jun 2015: uprev kilo
#  Dec 2014: uprev juno
#  Jul 2014: rename ironic
#  Dec 2013: uprev grizzly, havana
#  Nov 2013: integrate source from https://github.com/stackforge/puppet-sysinv
#

require 'spec_helper'
describe 'sysinv' do
  let :req_params do
    {:rabbit_password => 'guest', :sql_connection => 'mysql://user:password@host/database'}
  end

  let :facts do
    {:osfamily => 'Debian'}
  end

  describe 'with only required params' do
    let :params do
      req_params
    end

    it { should contain_class('sysinv::params') }

    it 'should contain default config' do
      should contain_sysinv_config('DEFAULT/rpc_backend').with(
        :value => 'sysinv.openstack.common.rpc.impl_kombu'
      )
      should contain_sysinv_config('DEFAULT/control_exchange').with(
        :value => 'openstack'
      )
      should contain_sysinv_config('DEFAULT/rabbit_password').with(
        :value => 'guest',
        :secret => true
      )
      should contain_sysinv_config('DEFAULT/rabbit_host').with(
        :value => '127.0.0.1'
      )
      should contain_sysinv_config('DEFAULT/rabbit_port').with(
        :value => '5672'
      )
      should contain_sysinv_config('DEFAULT/rabbit_hosts').with(
        :value => '127.0.0.1:5672'
      )
      should contain_sysinv_config('DEFAULT/rabbit_ha_queues').with(
        :value => false
      )
      should contain_sysinv_config('DEFAULT/rabbit_virtual_host').with(
        :value => '/'
      )
      should contain_sysinv_config('DEFAULT/rabbit_userid').with(
        :value => 'guest'
      )
      should contain_sysinv_config('DEFAULT/sql_connection').with(
        :value  => 'mysql://user:password@host/database',
        :secret => true
      )
      should contain_sysinv_config('DEFAULT/sql_idle_timeout').with(
        :value => '3600'
      )
      should contain_sysinv_config('DEFAULT/verbose').with(
        :value => false
      )
      should contain_sysinv_config('DEFAULT/debug').with(
        :value => false
      )
      should contain_sysinv_config('DEFAULT/api_paste_config').with(
        :value => '/etc/sysinv/api-paste.ini'
      )
    end

    it { should contain_file('/etc/sysinv/sysinv.conf').with(
      :owner   => 'sysinv',
      :group   => 'sysinv',
      :mode    => '0600',
      :require => 'Package[sysinv]'
    ) }

    it { should contain_file('/etc/sysinv/api-paste.ini').with(
      :owner   => 'sysinv',
      :group   => 'sysinv',
      :mode    => '0600',
      :require => 'Package[sysinv]'
    ) }

  end
  describe 'with modified rabbit_hosts' do
    let :params do
      req_params.merge({'rabbit_hosts' => ['rabbit1:5672', 'rabbit2:5672']})
    end

    it 'should contain many' do
      should_not contain_sysinv_config('DEFAULT/rabbit_host')
      should_not contain_sysinv_config('DEFAULT/rabbit_port')
      should contain_sysinv_config('DEFAULT/rabbit_hosts').with(
        :value => 'rabbit1:5672,rabbit2:5672'
      )
      should contain_sysinv_config('DEFAULT/rabbit_ha_queues').with(
        :value => true
      )
    end
  end

  describe 'with a single rabbit_hosts entry' do
    let :params do
      req_params.merge({'rabbit_hosts' => ['rabbit1:5672']})
    end

    it 'should contain many' do
      should_not contain_sysinv_config('DEFAULT/rabbit_host')
      should_not contain_sysinv_config('DEFAULT/rabbit_port')
      should contain_sysinv_config('DEFAULT/rabbit_hosts').with(
        :value => 'rabbit1:5672'
      )
      should contain_sysinv_config('DEFAULT/rabbit_ha_queues').with(
        :value => true
      )
    end
  end

  describe 'with qpid rpc supplied' do

    let :params do
      {
        :sql_connection      => 'mysql://user:password@host/database',
        :qpid_password       => 'guest',
        :rpc_backend         => 'sysinv.openstack.common.rpc.impl_qpid'
      }
    end

    it { should contain_sysinv_config('DEFAULT/sql_connection').with_value('mysql://user:password@host/database') }
    it { should contain_sysinv_config('DEFAULT/rpc_backend').with_value('sysinv.openstack.common.rpc.impl_qpid') }
    it { should contain_sysinv_config('DEFAULT/qpid_hostname').with_value('localhost') }
    it { should contain_sysinv_config('DEFAULT/qpid_port').with_value('5672') }
    it { should contain_sysinv_config('DEFAULT/qpid_username').with_value('guest') }
    it { should contain_sysinv_config('DEFAULT/qpid_password').with_value('guest').with_secret(true) }
    it { should contain_sysinv_config('DEFAULT/qpid_reconnect').with_value(true) }
    it { should contain_sysinv_config('DEFAULT/qpid_reconnect_timeout').with_value('0') }
    it { should contain_sysinv_config('DEFAULT/qpid_reconnect_limit').with_value('0') }
    it { should contain_sysinv_config('DEFAULT/qpid_reconnect_interval_min').with_value('0') }
    it { should contain_sysinv_config('DEFAULT/qpid_reconnect_interval_max').with_value('0') }
    it { should contain_sysinv_config('DEFAULT/qpid_reconnect_interval').with_value('0') }
    it { should contain_sysinv_config('DEFAULT/qpid_heartbeat').with_value('60') }
    it { should contain_sysinv_config('DEFAULT/qpid_protocol').with_value('tcp') }
    it { should contain_sysinv_config('DEFAULT/qpid_tcp_nodelay').with_value(true) }

  end

  describe 'with syslog disabled' do
    let :params do
      req_params
    end

    it { should contain_sysinv_config('DEFAULT/use_syslog').with_value(false) }
  end

  describe 'with syslog enabled' do
    let :params do
      req_params.merge({
        :use_syslog   => 'true',
      })
    end

    it { should contain_sysinv_config('DEFAULT/use_syslog').with_value(true) }
    it { should contain_sysinv_config('DEFAULT/syslog_log_facility').with_value('LOG_USER') }
  end

  describe 'with syslog enabled and custom settings' do
    let :params do
      req_params.merge({
        :use_syslog   => 'true',
        :log_facility => 'LOG_LOCAL0'
     })
    end

    it { should contain_sysinv_config('DEFAULT/use_syslog').with_value(true) }
    it { should contain_sysinv_config('DEFAULT/syslog_log_facility').with_value('LOG_LOCAL0') }
  end

end
