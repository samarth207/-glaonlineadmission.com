(() => {
    "use strict";

    const dialog = document.getElementById("admission-enquiry");
    const programs = [
        ["bcom", "BCOM_HONS"], ["bba", "BBA"], ["bca", "BCA"],
        ["mba", "MBA"], ["mca", "MCA"]
    ];
    const pageProgram = programs.find(([slug]) =>
        location.pathname.split("/").some(part => part === slug || part === `online-${slug}` || part === "online-bcom-hons" && slug === "bcom")
    );
    document.querySelectorAll('[data-local-form="enquiry"]').forEach(form => {
        if (pageProgram) form.elements.program.value = pageProgram[1];
    });

    document.querySelectorAll("[data-open-enquiry]").forEach(link => {
        link.addEventListener("click", event => {
            if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
            if (!dialog || typeof dialog.showModal !== "function") return;
            event.preventDefault();
            const form = dialog.querySelector("[data-local-form]");
            const brochure = link.dataset.brochure;
            if (brochure) {
                form.dataset.download = brochure;
                form.querySelector("h3").textContent = "Request a Program Brochure";
                form.querySelector('button[type="submit"]').textContent = "Save and Download Brochure";
            } else {
                delete form.dataset.download;
                form.querySelector("h3").textContent = "Enquire About Admissions";
                form.querySelector('button[type="submit"]').textContent = "Submit Enquiry";
            }
            dialog.showModal();
        });
    });
    document.querySelectorAll("[data-close-enquiry]").forEach(button => {
        button.addEventListener("click", () => dialog.close());
    });

    let tokenPromise;
    async function getToken() {
        if (!tokenPromise) {
            tokenPromise = (async () => {
                const response = await fetch("/api/form.php", { credentials: "same-origin", cache: "no-store" });
                const result = await response.json();
                if (!response.ok || typeof result.token !== "string") {
                    throw new Error(result.message || "The enquiry service is unavailable.");
                }
                return result.token;
            })();
        }
        try {
            return await tokenPromise;
        } catch (error) {
            tokenPromise = undefined;
            throw error;
        }
    }

    function newSubmissionId() {
        const bytes = crypto.getRandomValues(new Uint8Array(16));
        bytes[6] = (bytes[6] & 0x0f) | 0x40;
        bytes[8] = (bytes[8] & 0x3f) | 0x80;
        const hex = Array.from(bytes, byte => byte.toString(16).padStart(2, "0")).join("");
        return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`;
    }

    document.querySelectorAll("[data-local-form]").forEach(form => {
        let submissionId;
        form.addEventListener("submit", async event => {
            event.preventDefault();
            if (!form.reportValidity()) return;
            const button = form.querySelector('button[type="submit"]');
            if (button.disabled) return;
            const status = form.querySelector(".local-form-status");
            button.disabled = true;
            status.dataset.state = "pending";
            status.textContent = "Saving your enquiry...";

            try {
                submissionId ||= newSubmissionId();
                const values = Object.fromEntries(new FormData(form));
                const payload = {
                    ...values,
                    form_type: form.dataset.localForm,
                    consent: form.elements.consent.checked,
                    submission_id: submissionId,
                    source_path: location.pathname
                };
                const response = await fetch("/api/form.php", {
                    method: "POST",
                    credentials: "same-origin",
                    headers: { "Content-Type": "application/json", "X-CSRF-Token": await getToken() },
                    body: JSON.stringify(payload)
                });
                const result = await response.json();
                if (response.status === 403) tokenPromise = undefined;
                if (!response.ok || result.saved !== true) {
                    throw new Error(result.message || "Your enquiry could not be saved.");
                }
                status.dataset.state = "success";
                status.textContent = result.message;
                if (form.dataset.download) {
                    const download = document.createElement("a");
                    download.href = form.dataset.download;
                    download.download = "";
                    download.textContent = " Download brochure";
                    status.append(download);
                    download.click();
                }
                form.reset();
                submissionId = undefined;
                if (pageProgram && form.elements.program) form.elements.program.value = pageProgram[1];
            } catch (error) {
                console.error("Enquiry submission failed:", error);
                status.dataset.state = "error";
                status.textContent = error instanceof Error
                    ? `Not saved: ${error.message} Please try again or contact us by phone.`
                    : "Your enquiry could not be saved. Please contact us by phone.";
            } finally {
                button.disabled = false;
                status.focus();
            }
        });
    });

    const searchForm = document.getElementById("desktop_global_search");
    if (searchForm) {
        const searchButton = document.getElementById("searchBtn");
        searchButton?.addEventListener("click", event => {
            event.preventDefault();
            searchForm.requestSubmit();
        });
        searchForm.addEventListener("submit", async event => {
            event.preventDefault();
            const query = searchForm.elements.search.value.trim().toLowerCase();
            const output = document.getElementById("local-search-results");
            if (!query) return;
            output.replaceChildren();
            try {
                const response = await fetch("/siteassets/search-index.json");
                if (!response.ok) throw new Error("Search index is unavailable.");
                const pages = await response.json();
                const words = query.split(/\s+/);
                const results = pages.filter(entry => words.every(word =>
                    `${entry.title} ${entry.text}`.toLowerCase().includes(word)
                )).slice(0, 20);
                if (results.length === 0) output.textContent = "No matching pages found.";
                results.forEach(entry => {
                    const link = document.createElement("a");
                    link.href = entry.path;
                    link.textContent = entry.title;
                    output.append(link);
                });
            } catch (error) {
                console.error("Local search failed:", error);
                output.textContent = "Search is unavailable. Please use the navigation menu.";
            }
        });
    }

    document.querySelectorAll("[data-local-events]").forEach(list => {
        const filters = ["month", "batch", "year_search"];
        const cards = Array.from(list.children);
        filters.forEach(name => document.getElementById(name)?.addEventListener("change", () => {
            const month = document.getElementById("month")?.value || "";
            const year = document.getElementById("batch")?.value || document.getElementById("year_search")?.value || "";
            cards.forEach(card => {
                card.hidden = Boolean(month && card.dataset.month !== month || year && card.dataset.year !== year);
            });
        }));
    });
})();
