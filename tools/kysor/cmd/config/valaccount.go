package config

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	commoncmd "github.com/KYVENetwork/kyve-rdk/common/goutils/cmd"

	"github.com/knadh/koanf/parsers/toml"
	"github.com/knadh/koanf/providers/file"
	"github.com/knadh/koanf/v2"
	"github.com/spf13/cobra"
)

var (
	ValaccountConfigs       []ValaccountConfig
	ValaccountConfigOptions []commoncmd.Option[ValaccountConfig]
)

type ValaccountConfig struct {
	_    commoncmd.Option[ValaccountConfig]
	name string
	path string

	Pool           uint64 `koanf:"pool"`
	Valaccount     string `koanf:"valaccount"`
	StoragePriv    string `koanf:"storagePriv"`
	RequestBackoff string `koanf:"requestBackoff"`
	Cache          string `koanf:"cache"`
	Metrics        bool   `koanf:"metrics"`
	MetricsPort    uint64 `koanf:"metricsPort"`
}

func (c ValaccountConfig) Save(path string) error {
	return save(c, path)
}

func (c ValaccountConfig) Name() string {
	return c.name
}

func (c ValaccountConfig) Value() ValaccountConfig {
	return c
}

func (c ValaccountConfig) StringValue() string {
	return c.name + ".toml"
}

func (c ValaccountConfig) Path() string {
	return c.path
}

func (c ValaccountConfig) GetContainerLabel() string {
	return fmt.Sprintf("kysor-%s-%s", GetConfigX().GetChainPrettyName(), c.name)
}

func GetValaccountsConfigDir(cmd *cobra.Command) (string, error) {
	homeDir, err := GetHomeDir(cmd)
	if err != nil {
		return "", err
	}
	return filepath.Join(homeDir, "valaccounts"), nil
}

func loadValaccountConfigs(cmd *cobra.Command, _ []string) error {
	valaccountsDir, err := GetValaccountsConfigDir(cmd)
	if err != nil {
		return err
	}

	// Get all the valaccount config files
	entries, err := os.ReadDir(valaccountsDir)
	if err != nil && os.IsNotExist(err) {
		// return if the dir doesn't exist
		return nil
	} else if err != nil {
		return fmt.Errorf("error reading valaccount config directory: %s", err)
	}

	for _, entry := range entries {
		if !entry.IsDir() {
			if filepath.Ext(entry.Name()) == ".toml" {
				k := koanf.New(".")
				var valaccountConfig ValaccountConfig
				name := entry.Name()
				path := filepath.Join(valaccountsDir, entry.Name())
				err = k.Load(file.Provider(path), toml.Parser())
				if err != nil {
					return fmt.Errorf("error loading valaccount config file: %s", err)
				}
				err = k.Unmarshal("", &valaccountConfig)
				if err != nil {
					return fmt.Errorf("error unmarshalling valaccount config file: %s", err)
				}
				// Set the name without the extension
				valaccountConfig.name = strings.TrimSuffix(name, filepath.Ext(name))
				valaccountConfig.path = path
				ValaccountConfigs = append(ValaccountConfigs, valaccountConfig)
				ValaccountConfigOptions = append(ValaccountConfigOptions, valaccountConfig)
			}
		}
	}
	return nil
}
