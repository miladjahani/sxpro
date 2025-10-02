from playwright.sync_api import Page, expect

def test_simulation_run(page: Page):
    """
    This test verifies that the SimSXCu web application can successfully
    run a simulation in 'Designer Mode' and display the results.
    """
    # 1. Arrange: Go to the application's homepage.
    # The frontend server runs on port 3000.
    page.goto("http://localhost:3000")

    # 2. Act: Run the simulation.
    # We wait for the initial "Welcome" alert to ensure the app is ready.
    expect(page.get_by_text("Welcome to SimSXCu")).to_be_visible(timeout=15000)

    # Find the "Run Simulation" button and click it.
    run_button = page.get_by_role("button", name="Run Simulation")
    run_button.click()

    # 3. Assert: Wait for the results to be displayed.
    # The "Optimal Extractant" card is a key indicator of a successful run.
    # We give it a longer timeout to allow for the backend calculation.
    expect(page.get_by_text("Optimal Extractant")).to_be_visible(timeout=20000)

    # Also check for the McCabe-Thiele plot to ensure visualizations are rendered.
    expect(page.get_by_text("Extraction McCabe-Thiele")).to_be_visible()

    # 4. Screenshot: Capture the final state of the application.
    page.screenshot(path="jules-scratch/verification/simulation_result.png")