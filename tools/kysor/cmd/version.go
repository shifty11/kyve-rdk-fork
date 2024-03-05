package cmd

import (
	"fmt"
	"runtime"

	"github.com/spf13/cobra"
)

var (
	Version = "(none)"
	Commit  = "(none)"
	Tag     = ""
)

func versionCmd() *cobra.Command {
	return &cobra.Command{
		Use:   "version",
		Short: "Show KYSOR version",
		Run: func(cmd *cobra.Command, args []string) {
			fmt.Printf("Kysor version: %s\n", Version)
			if Tag != "" {
				fmt.Printf("Git tag: %s\n", Tag)
			}
			fmt.Printf("Git commit: %s\n", Commit)
			fmt.Println()
			fmt.Printf("Go version: %s\n", runtime.Version())
			fmt.Println()
			fmt.Printf("Platform: %s\n", runtime.GOOS)
			fmt.Printf("Arch: %s\n", runtime.GOARCH)
		},
	}
}

func init() {
	rootCmd.AddCommand(versionCmd())
}
