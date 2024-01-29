package docker

import (
	"context"
	"fmt"
	"github.com/docker/docker/api/types"
	"github.com/docker/docker/api/types/container"
	"github.com/docker/docker/api/types/filters"
	"github.com/docker/docker/api/types/network"
	"github.com/docker/docker/client"
)

type NetworkConfig struct {
	Name   string
	Labels map[string]string
}

type ContainerConfig struct {
	Image   string
	Name    string
	Network NetworkConfig
	User    string
	Env     []string
	Binds   []string
	Cmd     []string
}

func createNetwork(ctx context.Context, cli *client.Client, network NetworkConfig) error {
	networks, err := cli.NetworkList(ctx, types.NetworkListOptions{})
	if err != nil {
		return err
	}

	// Return if network already exists (by name)
	for _, net := range networks {
		if net.Name == network.Name {
			return nil
		}
	}

	// Create network
	_, err = cli.NetworkCreate(ctx, network.Name, types.NetworkCreate{
		Labels: network.Labels,
	})
	return err
}

func StartContainer(ctx context.Context, cli *client.Client, config ContainerConfig) (string, error) {
	var endpointsConfig map[string]*network.EndpointSettings
	if config.Network.Name != "" {
		err := createNetwork(ctx, cli, config.Network)
		if err != nil {
			return "", err
		}
		endpointsConfig = map[string]*network.EndpointSettings{
			config.Network.Name: {},
		}
	}

	r, err := cli.ContainerCreate(
		ctx,
		&container.Config{
			Image: config.Image,
			Env:   config.Env,
			Cmd:   config.Cmd,
			User:  config.User,
		},
		&container.HostConfig{
			Binds: config.Binds,
		},
		&network.NetworkingConfig{
			EndpointsConfig: endpointsConfig,
		},
		nil,
		config.Name,
	)
	if err != nil {
		return "", err
	}

	err = cli.ContainerStart(ctx, r.ID, types.ContainerStartOptions{})
	if err != nil {
		return "", err
	}
	return r.ID, nil
}

func RemoveContainers(ctx context.Context, cli *client.Client, label string) error {
	// Get all containers with "label"
	containers, err := cli.ContainerList(ctx, types.ContainerListOptions{
		All: true,
		Filters: filters.NewArgs(
			filters.Arg("label", fmt.Sprintf("%s=", label)),
		),
	})
	if err != nil {
		return err
	}

	// Remove the containers
	for _, cont := range containers {
		err = cli.ContainerRemove(ctx, cont.ID, types.ContainerRemoveOptions{
			Force: true,
		})
		if err != nil {
			return err
		}
	}
	return nil
}

func RemoveNetworks(ctx context.Context, cli *client.Client, label string) error {
	// Get all networks with "label"
	networks, err := cli.NetworkList(ctx, types.NetworkListOptions{
		Filters: filters.NewArgs(
			filters.Arg("label", fmt.Sprintf("%s=", label)),
		),
	})
	if err != nil {
		return err
	}

	// Remove the networks
	for _, net := range networks {
		err = cli.NetworkRemove(ctx, net.ID)
		if err != nil {
			return err
		}
	}
	return nil
}
